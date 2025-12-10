from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from sqlalchemy import select

from core.db import SessionLocal
from core.models import User

router = Router()


def _last_word(text: str) -> str:
    return (text or "").strip().split(maxsplit=1)[-1]


@router.message(lambda m: _last_word(m.text or "") == "Сообщество")
async def community_handler(message: Message, state: FSMContext):
    """Раздел 'Сообщество' — заглушка + заявка на вступление."""
    await state.clear()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Хочу вступить", callback_data="want_community")]
        ]
    )

    text = (
        "👥 Раздел <b>«Сообщество»</b> появится позже.\n"
        "Мы готовим тематические группы и новые форматы общения.\n\n"
        "Если вы хотите вступить в сообщество, нажмите кнопку ниже — "
        "мы уведомим вас при запуске."
    )

    await message.answer(text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data == "want_community")
async def community_join_callback(call: CallbackQuery):
    """Пользователь нажал 'Хочу вступить'."""
    tg_id = call.from_user.id

    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(telegram_id=tg_id))
        user = result.scalars().first()
        if user:
            user.wants_community = True
            await session.commit()

    await call.message.edit_text(
        "✅ Спасибо! Мы отметили вашу готовность вступить в сообщество.\n"
        "Как только раздел будет запущен, мы вас уведомим."
    )
    await call.answer()
