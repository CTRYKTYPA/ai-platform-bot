from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки главного меню (важно: text=..., а не позиционный аргумент)
btn_ai = KeyboardButton(text="🤖 ИИ-Проводник")     # AI Guide/Dialogue
btn_material_day = KeyboardButton(text="📖 Материал дня")
btn_materials = KeyboardButton(text="🗂 Материалы")
btn_programs = KeyboardButton(text="🧭 Программы")
btn_meetings = KeyboardButton(text="📅 Встречи")
btn_community = KeyboardButton(text="👥 Сообщество")
btn_profile = KeyboardButton(text="👤 Профиль")

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [btn_ai],
        [btn_material_day],
        [btn_materials],
        [btn_programs],
        [btn_meetings],
        [btn_community],
        [btn_profile],
    ],
    resize_keyboard=True,
)
