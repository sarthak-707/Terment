from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from rich.console import Console

from terment.providers import Provider

console = Console()


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

    def _initialise_context(self):
        if self.system_prompt is not None:
            self.messages.append({"role": "system", "content": self.system_prompt})

    def _generate_response(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})
        stream = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            stream=True,
            reasoning_effort="none",
        )
        final_response_list = []
        for chunks in stream:
            content = chunks.choices[0].delta.content
            if content is not None:
                final_response_list.append(content)
                final_response = "".join(final_response_list)
                yield final_response
        self.messages.append({"role": "assistant", "content": final_response})
