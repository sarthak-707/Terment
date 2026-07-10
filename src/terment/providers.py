import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Provider:
    name: str
    api_key: str
    base_url: str


openrouter = Provider(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY", ""),
    name="openrouter",
)

openai = Provider(
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY", ""),
    name="openai",
)

gemini = Provider(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY", ""),
    name="gemini",
)

groq = Provider(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY", ""),
    name="groq",
)

nvidia = Provider(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY", ""),
    name="nvidia",
)

llama_cpp = Provider(
    base_url="http://localhost:8080/v1", api_key="Not-Needed", name="llama_cpp"
)

provider_list = [openrouter, openai, gemini, groq, nvidia, llama_cpp]
