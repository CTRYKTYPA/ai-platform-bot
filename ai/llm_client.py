import asyncio

async def get_llm_answer(question: str) -> str:
    """
    Stub for LLM API call.
    In future, this will call the actual LLM (OpenAI, etc.) to get an answer.
    """

    await asyncio.sleep(0)

    return f"🤖 [ИИ]: Ваш вопрос — \"{question}\".\nОтвет: (заглушка ИИ-ответа)."
