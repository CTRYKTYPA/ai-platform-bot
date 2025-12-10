# AI Platform Bot — MVP (Этап 1)

Telegram-бот-платформа с ИИ-ответами, контентными разделами, программами, встречами и подпиской.  
Данный репозиторий содержит реализацию **Этапа 1**: архитектура, БД, каркас backend-а и бота, базовая авторизация и LLM-заглушка.

## Технологический стек

- Python 3.11
- aiogram 3.22.0 — Telegram-бот
- FastAPI — backend / админ API (каркас)
- SQLAlchemy 2.x — ORM
- PostgreSQL / SQLite — БД (для локального запуска можно использовать SQLite)
- asyncpg / aiosqlite — драйверы БД

## Структура проекта

ai_platform_bot/
├── core/              # Конфигурация, БД, ORM-модели, сервисы
├── bot/               # Telegram-бот (хендлеры, клавиатуры, точка входа)
├── ai/                # LLM-клиент (заглушка для ИИ-ответов)
├── admin/             # FastAPI-приложение для админ-панели (каркас)
├── create_db.py       # Скрипт создания схемы БД
├── seed_materials.py  # Пример наполнения тестовыми материалами
└── requirements.txt
Настройка и запуск локально
1. Клонировать репозиторий
git clone https://github.com/CTRYKTYPA/ai-platform-bot.git
cd ai-platform-bot
2. Виртуальное окружение и зависимости
python -m venv .venv
.\.venv\Scripts\activate        # Windows
pip install -r requirements.txt
3. Настройка конфигурации
В файле core/config.py нужно указать:

BOT_TOKEN — токен Telegram-бота от @BotFather

DATABASE_URL — строку подключения к БД.

Примеры:

python
# Пример для SQLite (для локального запуска)
DATABASE_URL = "sqlite+aiosqlite:///./dev.db"

# Пример для PostgreSQL
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/ai_platform_db"
4. Создать схему БД

python create_db.py
5. Запуск бота

python -m bot.main
После запуска:

отправить /start боту в Telegram;

проверить главное меню и разделы:

«Материал дня»

«Материалы»

«Программы»

«Встречи»

«Сообщество» (заглушка с кнопкой «Хочу вступить»)

«Профиль» (статус, уведомления, сброс прогресса);

протестировать ИИ-диалог (любой текстовый вопрос → ответ заглушки + запись в qa_log).

6. (Опционально) запуск admin API

uvicorn admin.main:app --reload
Проверка:

http://127.0.0.1:8000/ → {"status": "ok", "message": "Admin panel is running."}

http://127.0.0.1:8000/docs → Swagger-документация FastAPI.

На данном этапе admin-сервис выступает как каркас для будущей админ-панели.
