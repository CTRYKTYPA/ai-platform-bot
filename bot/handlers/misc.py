from aiogram import Router
from aiogram.types import Message
from sqlalchemy import select

from core.db import SessionLocal
from core.models import User, QALog
from ai.llm_client import get_llm_answer

router = Router()


MENU_KEYWORDS = [
    "ИИ-Проводник",
    "Материал дня",
    "Материалы",
    "Программы",
    "Встречи",
    "Сообщество",
    "Профиль",
]


@router.message()
async def fallback_text_handler(message: Message):
    """
    Любой текст, который не поймали другие хендлеры
    и НЕ является текстом кнопки меню, считаем вопросом к ИИ.
    """
    text = (message.text or "").strip()
    if not text:
        return

    # Если сообщение похоже на нажатие одной из кнопок меню — выходим.
    if any(keyword in text for keyword in MENU_KEYWORDS):
        return

    # Всё остальное — вопрос к ИИ
    user_tg = message.from_user
    answer = await get_llm_answer(text)
    await message.answer(answer)

    async with SessionLocal() as session:
        result = await session.execute(
            select(User.id).filter_by(telegram_id=user_tg.id)
        )
        user_id = result.scalar_one_or_none()

        if user_id:
            log = QALog(user_id=user_id, question=text, answer=answer)
            session.add(log)
            await session.commit()
