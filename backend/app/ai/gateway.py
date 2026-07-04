from app.ai.providers.ollama_provider import OllamaProvider


class AIGateway:
    def __init__(self) -> None:
        self.llm = OllamaProvider()

    async def generate_chinese_words(self, topic: str) -> dict:
        prompt = (
            "너는 중국어 교육 콘텐츠 생성기다. "
            f"주제 '{topic}'와 관련된 중국어 단어 3개를 JSON으로 생성해. "
            "필드는 word, pinyin, meaning, sentence, translation 을 사용해. "
            "반드시 JSON만 출력해."
        )
        return await self.llm.generate_json(prompt)


ai_gateway = AIGateway()
