import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Provider:
    api_key: str
    base_url: str


openrouter = Provider(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY", "")
)

# openai = Provider(
#     base_url="https://api.openai.com/v1", api_key=os.getenv("OPENAI_API_KEY", "")
# )

gemini = Provider(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY", ""),
)
