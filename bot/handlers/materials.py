from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


def _last_word(text: str) -> str:
    return (text or "").strip().split(maxsplit=1)[-1]


@router.message(lambda m: _last_word(m.text or "") == "Материалы")
async def materials_handler(message: Message, state: FSMContext):
    """Раздел 'Материалы' (заглушка)."""
    await state.clear()
    await message.answer(
        "📂 Раздел «Материалы»: здесь будут тематические категории и подборки. (В разработке)"
    )
