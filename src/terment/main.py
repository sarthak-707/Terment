import time
import json
from openai import OpenAI
from openai import APIConnectionError
from openai.types.chat import ChatCompletionMessageParam
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from collections.abc import Generator
from pathlib import Path

from terment.providers import (
    Provider,
    gemini,
    openrouter,
    groq,
    openai,
    nvidia,
    llama_cpp,
)

load_dotenv()
console = Console()

list_of_providers: list[Provider] = [
    openai,
    gemini,
    groq,
    openrouter,
    nvidia,
    llama_cpp,
]


class Chatbot:
    def __init__(
        self, model: str, provider: Provider, system_prompt: str | None
    ) -> None:
        if provider.api_key == "":
            raise ValueError("Api Key not found for the selected provider.")
        self.messages: list[ChatCompletionMessageParam] = []
        self.client = OpenAI(api_key=provider.api_key, base_url=provider.base_url)
        self.model = model
        self.system_prompt = system_prompt
        if self.system_prompt is not None:
            self.messages.append({"role": "system", "content": self.system_prompt})

    def _generate_response(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})
        stream = self.client.chat.completions.create(
            messages=self.messages, model=self.model, stream=True
        )
        final_response_list = []
        for chunks in stream:
            content = chunks.choices[0].delta.content
            if content is not None:
                final_response_list.append(content)
                final_response = "".join(final_response_list)
                yield final_response
        self.messages.append({"role": "assistant", "content": final_response})

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
        file_name = Path("sessions") / f"{time.strftime('%y%b%d%H%M%S')}"
        Path.touch(file_name)
        with open(
            f"{file_name}.json", "w", encoding="utf-8"
        ) as conversation_history_file:
            json.dump(self.messages, conversation_history_file, indent=4)

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


terment = Chatbot(
    model="LFM2.5-350M-Q4_K_M.gguf",
    provider=llama_cpp,
    system_prompt="You are a helpful agent which uses dry humour with a cozy tone .",
)


def main():
    try:
        terment.terminal_chat()
    except APIConnectionError:
        print("Failed to Connect with the servers")


if __name__ == "__main__":
    main()
