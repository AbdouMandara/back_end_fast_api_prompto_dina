from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    hf_token: Optional[str] = None
    default_provider: str = "huggingface"
    hf_router_url: str = "https://router.huggingface.co/v1"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
