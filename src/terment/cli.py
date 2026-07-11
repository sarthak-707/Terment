from time import strftime
from json import dump
from rich.panel import Panel
from rich.markdown import Markdown
from collections.abc import Generator
from rich.live import Live
from rich.console import Console
from pathlib import Path
from openai import APIConnectionError
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


from terment.config_manager import get_selected_provider
from terment.chatbot import Chatbot

console = Console()


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
        file_name = Path("sessions") / f"{strftime('%y%b%d%H%M%S')}"
        Path.touch(file_name)
        with open(
            f"{file_name}.json", "w", encoding="utf-8"
        ) as conversation_history_file:
            dump(self.messages, conversation_history_file, indent=4)

    def terminal_chat(self) -> None:
        while True:
            try:
                prompt = input("You : ")
            except KeyboardInterrupt:
                print("\nExiting")
                self._save_chat()
                break
            if prompt.lower() in ["bye", "exit", "quit"]:
                print("\nExiting !")
                self._save_chat()
                break
            ai_response = self._generate_response(prompt)
            self._render_message(ai_response)


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
