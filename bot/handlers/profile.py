from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from sqlalchemy import select, delete

from core.db import SessionLocal
from core.models import User, UserProgramProgress

router = Router()


def _last_word(text: str) -> str:
    return (text or "").strip().split(maxsplit=1)[-1]


def _status_text(user: User | None) -> str:
    if not user:
        return "Бесплатный доступ"
    if user.status == "paid":
        return "Подписка (paid) ✅"
    if user.status == "donor":
        return "Поддерживающий донор ❤️"
    return "Бесплатный доступ"


@router.message(lambda m: _last_word(m.text or "") == "Профиль")
async def profile_handler(message: Message, state: FSMContext):
    """Профиль пользователя: статус и настройки уведомлений."""
    await state.clear()

    async with SessionLocal() as session:
        result = await session.execute(
            select(User).filter_by(telegram_id=message.from_user.id)
        )
        user = result.scalars().first()

    status_text = _status_text(user)
    notif_text = (
        "включены ✅"
        if user and user.notifications_enabled
        else "отключены ❌"
    )

    profile_text = (
        f"👤 <b>Ваш профиль</b>\n"
        f"Статус: {status_text}\n"
        f"Уведомления: {notif_text}"
    )

    toggle_label = (
        "Отключить уведомления"
        if user and user.notifications_enabled
        else "Включить уведомления"
    )

    buttons = [
        [InlineKeyboardButton(text=toggle_label, callback_data="toggle_notifs")],
        [InlineKeyboardButton(text="Сбросить прогресс", callback_data="reset_progress")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(profile_text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data == "toggle_notifs")
async def toggle_notifications_handler(call: CallbackQuery):
    """Вкл/выкл уведомления пользователя."""
    tg_id = call.from_user.id

    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(telegram_id=tg_id))
        user = result.scalars().first()

        if not user:
            await call.answer("Профиль не найден.", show_alert=True)
            return

        user.notifications_enabled = not user.notifications_enabled
        await session.commit()

        status_text = _status_text(user)
        notif_text = (
            "включены ✅" if user.notifications_enabled else "отключены ❌"
        )

        new_text = (
            f"👤 <b>Ваш профиль</b>\n"
            f"Статус: {status_text}\n"
            f"Уведомления: {notif_text}"
        )

        new_toggle_label = (
            "Отключить уведомления"
            if user.notifications_enabled
            else "Включить уведомления"
        )

        new_buttons = [
            [InlineKeyboardButton(text=new_toggle_label, callback_data="toggle_notifs")],
            [InlineKeyboardButton(text="Сбросить прогресс", callback_data="reset_progress")],
        ]
        new_keyboard = InlineKeyboardMarkup(inline_keyboard=new_buttons)

    await call.message.edit_text(new_text, reply_markup=new_keyboard)
    await call.answer()


@router.callback_query(lambda c: c.data == "reset_progress")
async def reset_progress_handler(call: CallbackQuery):
    """Сброс прогресса по программам."""
    tg_id = call.from_user.id

    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(telegram_id=tg_id))
        user = result.scalars().first()

        if user:
            await session.execute(
                delete(UserProgramProgress).where(
                    UserProgramProgress.user_id == user.id
                )
            )
            await session.commit()

    await call.answer("✅ Прогресс по всем программам сброшен.", show_alert=True)
