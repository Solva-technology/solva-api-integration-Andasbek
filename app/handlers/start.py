from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from app.keyboards.inline import start_keyboard

router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот-погодник. Выбери интересующую тебя команду:", 
        reply_markup=start_keyboard()
    )