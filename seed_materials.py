import asyncio
from datetime import date, timedelta

from sqlalchemy import select

from core.db import SessionLocal
from core.models import Material, Category, User


async def seed():
    async with SessionLocal() as session:
        # Категория, если нужно
        result_cat = await session.execute(
            select(Category).filter_by(title="Базовая категория")
        )
        category = result_cat.scalars().first()
        if not category:
            category = Category(title="Базовая категория", description="Для теста")
            session.add(category)
            await session.flush()

        today = date.today()

        # FREE материал на сегодня
        free_mat = Material(
            title="Тестовый бесплатный материал дня",
            content="Это пример материала дня, доступный всем пользователям.",
            content_type="text",
            category=category,
            access_level="free",
            scheduled_date=today,
        )

        # PAID материал на завтра (для демонстрации логики доступа)
        paid_mat = Material(
            title="Тестовый платный материал дня",
            content="Это пример материала только для подписчиков.",
            content_type="text",
            category=category,
            access_level="paid",
            scheduled_date=today + timedelta(days=1),
        )

        session.add_all([free_mat, paid_mat])
        await session.commit()

    print("Тестовые материалы добавлены.")


if __name__ == "__main__":
    asyncio.run(seed())
