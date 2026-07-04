import json
import httpx

from app.ai.providers.base import BaseLLMProvider
from app.core.config import settings


class OllamaProvider(BaseLLMProvider):
    async def generate_json(self, prompt: str) -> dict:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": 0.6, "top_p": 0.9},
                },
            )
            response.raise_for_status()
            raw = response.json().get("response", "{}")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"raw": raw}
