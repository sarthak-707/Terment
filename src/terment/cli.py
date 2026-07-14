import subprocess
import platform
from time import strftime
from json import dump
from typing import Iterable
from prompt_toolkit.document import Document
from rich.panel import Panel
from rich import print as rprint
from rich.markdown import Markdown
from collections.abc import Generator
from rich.live import Live
from rich.console import Console
from pathlib import Path
from openai import APIConnectionError
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import (
    CompleteEvent,
    Completer,
    Completion,
)

from terment.config_manager import get_selected_provider
from terment.chatbot import Chatbot

console = Console()

SESSION_DIR = Path.home() / ".terment" / "sessions"
SESSION_DIR.mkdir(parents=True, exist_ok=True)


slash_commands = {
    "/exit": "Quit and save the session",
    "/clear": "Clear and start a new session",
}

prompt_style = Style.from_dict({"prompt": "bold #cba6f7"})


class SlashCommandCompleter(Completer):
    def __init__(self, slash_commands: dict) -> None:
        self.slash_commands = slash_commands

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion] | None:
        text = document.text_before_cursor

        if " " in text:
            return

        if not text.startswith("/"):
            return

        for cmd, description in self.slash_commands.items():
            if cmd.startswith(text):
                yield Completion(
                    cmd, start_position=-len(text), display_meta=description
                )


prompt_comnpleter = SlashCommandCompleter(slash_commands=slash_commands)


class CliChatbot(Chatbot):
    def _render_message(self, streamed_response: Generator) -> None:
        panel = Panel(
            renderable="",
            border_style="#ea76cb",
            title="Terment🤖",
            subtitle=self.model,
            padding=2,
        )
        with Live(panel, refresh_per_second=3, console=console) as live:
            for chunk in streamed_response:
                panel.renderable = Markdown(
                    chunk, style="#f9e2af", code_theme="catppuccin-mocha"
                )
                live.refresh()

    def _save_chat(self):
        file_name = SESSION_DIR / f"{strftime('%y%b%d%H%M%S')}.json"
        Path.touch(file_name)
        with open(file_name, "w", encoding="utf-8") as conversation_history_file:
            dump(self.messages, conversation_history_file, indent=4)

    def terminal_chat(self) -> None:
        self._initialise_context()
        while True:
            try:
                user_prompt = prompt(
                    "You : ", completer=prompt_comnpleter, style=prompt_style
                )
                if user_prompt.startswith("/"):
                    slash_command = user_prompt.split()[0]
                    if slash_command == "/exit":
                        rprint("[#f9e2af]\nExiting![/#f9e2af]")
                        self._save_chat()
                        print("Chat was saved.")
                        break
                    if slash_command == "/clear":
                        subprocess.run(
                            ["cls"] if platform.system == "Windows" else ["clear"]
                        )
                        self._save_chat()
                        self.messages.clear()
                        self._initialise_context()
                        rprint("[#f9e2af]\nConversation Saved![/#f9e2af]")

                else:
                    ai_response = self._generate_response(user_prompt)
                    self._render_message(ai_response)

            except KeyboardInterrupt:
                print("\nExiting")
                self._save_chat()
                break


selected_provider_dict = get_selected_provider()
selected_model = selected_provider_dict.get("model", None)
selected_provider = selected_provider_dict.get("provider", None)

if selected_provider is not None and selected_model is not None:
    terment = CliChatbot(
        model=selected_model,
        provider=selected_provider,
        system_prompt="You are a helpful agent which uses dry humour with a cozy tone .",
    )


def main():
    try:
        terment.terminal_chat()
    except APIConnectionError:
        print("Failed to Connect with the servers")
