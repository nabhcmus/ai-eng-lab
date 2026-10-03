from openai import OpenAI


def get_client(
    base_url: str = "http://localhost:11434/v1", api_key: str = "ollama"
) -> OpenAI:
    return OpenAI(base_url=base_url, api_key=api_key)


def ask(prompt: str, model: str = "qwen3:8b", client: OpenAI | None = None) -> str:
    client = client or get_client()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content or ""
