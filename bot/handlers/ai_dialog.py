from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select

from core.db import SessionLocal
from core.models import User, QALog
from ai.llm_client import get_llm_answer

router = Router()

# Ключевые слова кнопок (без привязки к эмодзи)
MENU_KEYWORDS = [
    "ИИ-Проводник",
    "Материал дня",
    "Материалы",
    "Программы",
    "Встречи",
    "Сообщество",
    "Профиль",
]


@router.message(F.text.contains("ИИ-Проводник"))
async def ai_intro(message: Message):
    """
    Нажали кнопку 'ИИ-Проводник' — просто подсказка,
    дальше пользователь может писать вопросы в свободной форме.
    """
    await message.answer(
        "💡 Вы перешли в режим ИИ-диалога.\n"
        "Напишите свой вопрос, и я постараюсь помочь."
    )


@router.message(
    lambda m: (m.text or "").strip()                          # есть текст
    and not any(k in m.text for k in MENU_KEYWORDS)           # и это НЕ кнопка меню
)
async def handle_ai_question(message: Message):
    """
    Любой текст, который не является нажатием кнопки меню,
    считаем вопросом к ИИ.
    """
    user_tg = message.from_user
    question_text = (message.text or "").strip()

    # Вызов заглушки ИИ
    answer_text = await get_llm_answer(question_text)
    await message.answer(answer_text)

    # Логируем в БД
    async with SessionLocal() as session:
        result = await session.execute(
            select(User.id).filter_by(telegram_id=user_tg.id)
        )
        user_id = result.scalar_one_or_none()

        if user_id:
            log_entry = QALog(
                user_id=user_id,
                question=question_text,
                answer=answer_text,
            )
            session.add(log_entry)
            await session.commit()
