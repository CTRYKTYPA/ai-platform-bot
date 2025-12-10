from datetime import date

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select

from core.db import SessionLocal
from core.models import User, Material

router = Router()


def _last_word(text: str) -> str:
    return (text or "").strip().split(maxsplit=1)[-1]


@router.message(lambda m: _last_word(m.text or "") == "Материал дня")
async def material_of_day_handler(message: Message, state: FSMContext):
    """Обработчик кнопки 'Материал дня'."""
    await state.clear()
    today = date.today()

    async with SessionLocal() as session:
        result_user = await session.execute(
            select(User).filter_by(telegram_id=message.from_user.id)
        )
        user = result_user.scalars().first()
        user_status = user.status if user else "free"

        result_mat = await session.execute(
            select(Material).filter_by(scheduled_date=today)
        )
        material = result_mat.scalars().first()

        if not material:
            await message.answer("📖 На сегодня нет материала. Загляните позже!")
            return

        if material.access_level in ("paid", "donor") and user_status == "free":
            await message.answer(
                "📖 Материал дня доступен только для подписчиков.\n"
                "Оформите подписку, чтобы получать расширенные материалы."
            )
            return

        response_text = (
            f"📖 <b>Материал дня</b>\n"
            f"<b>{material.title}</b>\n\n"
            f"{material.content or ''}"
        )
        await message.answer(response_text)
