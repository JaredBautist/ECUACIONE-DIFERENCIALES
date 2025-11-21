import httpx

from ..config import settings


async def ask_qwen(prompt: str) -> str:
    """Solicita validación o explicación a Qwen. Devuelve string (o mensaje si no hay API key)."""
    if not settings.QWEN_API_KEY:
        return "Qwen no configurado (falta QWEN_API_KEY)."

    headers = {"Authorization": f"Bearer {settings.QWEN_API_KEY}"}
    payload = {
        "model": settings.QWEN_MODEL,
        "input": prompt,
        "parameters": {"max_tokens": 512},
    }
    async with httpx.AsyncClient(timeout=settings.QWEN_TIMEOUT) as client:
        resp = await client.post(settings.QWEN_ENDPOINT, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("output_text") or str(data)
