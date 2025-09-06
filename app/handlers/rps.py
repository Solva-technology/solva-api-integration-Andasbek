from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.inline import rps_menu_keyboard, rps_again_keyboard
from app.services.rps import play

router = Router(name="rps")


@router.callback_query(F.data == "rps:menu")
async def rps_menu(cb: CallbackQuery):
    await cb.message.edit_text("Выберите жест:", reply_markup=rps_menu_keyboard())
    await cb.answer()


@router.callback_query(F.data.startswith("rps:pick:"))
async def rps_pick(cb: CallbackQuery):
    move = cb.data.split(":", 2)[-1]  # rock|paper|scissors
    bot_move, outcome = play(move)  # deterministic in tests via mock

    symbols = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
    rus = {"win": "Вы выиграли! 🎉", "lose": "Вы проиграли 😅", "draw": "Ничья 🤝"}

    text = (
        f"Вы выбрали: {symbols.get(move, move)}\n"
        f"Бот выбрал: {symbols.get(bot_move, bot_move)}\n\n"
        f"{rus[outcome]}"
    )
    await cb.message.edit_text(text, reply_markup=rps_again_keyboard())
    await cb.answer()
