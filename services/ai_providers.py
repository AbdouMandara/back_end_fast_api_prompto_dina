import logging
from enum import Enum
from typing import Optional

import httpx

from core.config import settings

logger = logging.getLogger('prompto_dina')


class Provider(str, Enum):
    huggingface = "huggingface"


def get_api_token(provider: Provider) -> Optional[str]:
    return settings.hf_token


def build_huggingface_messages(prompt: str) -> list[dict]:
    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                }
            ],
        }
    ]


def call_huggingface_router(prompt: str, model: str = "google/gemma-4-31B-it:novita") -> str:
    token = get_api_token(Provider.huggingface)
    if not token:
        raise ValueError("HF_TOKEN is required for the Hugging Face inference provider.")

    url = f"{settings.hf_router_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": build_huggingface_messages(prompt),
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    logger.info('HF router response keys: %s', list(data.keys()))
    choice = data.get("choices", [{}])[0]
    message = choice.get("message")
    if isinstance(message, dict):
        content = message.get("content")
        if isinstance(content, list) and content:
            item = content[0]
            return item.get("text", "") if isinstance(item, dict) else str(item)
        return str(content)
    return str(message)

