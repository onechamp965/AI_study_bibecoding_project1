from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_json(self, prompt: str) -> dict:
        raise NotImplementedError
