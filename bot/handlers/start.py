from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.keyboards.main_menu import main_menu_kb
from core.db import SessionLocal
from core.services.user_service import get_or_create_user

router = Router()

@router.message(CommandStart())
async def cmd_start_handler(message: Message):
    """Handle the /start command: register user and show welcome message with main menu."""
    user_tg = message.from_user

    tg_id = user_tg.id
    username = user_tg.username or ""
    full_name = f"{user_tg.first_name} {user_tg.last_name or ''}".strip()

    async with SessionLocal() as session:
        await get_or_create_user(session, telegram_id=tg_id, username=username, full_name=full_name)
        await session.commit()

    welcome_text = (
        f"Привет, {user_tg.first_name}! 👋\n"
        "Добро пожаловать в бота-платформу.\n"
        "Вы можете использовать меню ниже для навигации по разделам."
    )
    await message.answer(welcome_text, reply_markup=main_menu_kb)

