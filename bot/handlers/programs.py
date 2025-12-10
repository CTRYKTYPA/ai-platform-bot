from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


def _last_word(text: str) -> str:
    return (text or "").strip().split(maxsplit=1)[-1]


@router.message(lambda m: _last_word(m.text or "") == "Программы")
async def programs_handler(message: Message, state: FSMContext):
    """Раздел 'Программы' (заглушка)."""
    await state.clear()
    await message.answer(
        "🧭 Раздел «Программы»: здесь будет список программ и ваш прогресс. (MVP готовится)"
    )
