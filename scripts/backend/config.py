import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Configuración del backend y llaves de terceros."""

    QWEN_API_KEY: str | None = os.getenv("QWEN_API_KEY")
    QWEN_ENDPOINT: str = os.getenv(
        "QWEN_ENDPOINT",
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
    )
    QWEN_MODEL: str = os.getenv("QWEN_MODEL", "qwen-plus")
    QWEN_TIMEOUT: int = int(os.getenv("QWEN_TIMEOUT", "20"))


settings = Settings()
