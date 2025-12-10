import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import BOT_TOKEN
from bot.handlers import (
    start,
    ai_dialog,
    material_day,
    materials,
    programs,
    meetings,
    community,
    profile,
)


async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting bot...")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(material_day.router)
    dp.include_router(materials.router)
    dp.include_router(programs.router)
    dp.include_router(meetings.router)
    dp.include_router(community.router)
    dp.include_router(profile.router)
    dp.include_router(ai_dialog.router)  # AI-диалог в самом конце

    logger.info("Polling started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
