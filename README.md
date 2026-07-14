# Terment

A simple terminal chatbot built with Python, OpenAI-compatible API, Rich, and uv. Uses Catppuccin mocha theme.

## Features

- Streaming responses
- Rich terminal UI
- OpenAI-compatible providers (OpenRouter, OpenAI, Gemini, Groq, NVIDIA, llama.cpp)
- Conversation memory with session save on exit

## How to use
- Run `uv venv` then `uv sync`
- Copy `.env.example` to `.env` and add your API key
- Copy `config.yaml.example` to `~/.terment/config.yaml` and set your model/provider
- Run with `uv run terment`
- Exit with `bye`, `exit`, `quit`, or Ctrl+C (session saved to `~/.terment/sessions/`)

## Screenshot
![Terminal Example](terminal_example.png)
