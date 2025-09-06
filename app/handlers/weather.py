import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.keyboards.inline import weather_city_keyboard
from app.services.weather_client import WeatherClient, WeatherError
from app.services.mongo_client import Mongo
from app.services.sessions import record, is_blocked

router = Router(name="weather")
logger = logging.getLogger("app.weather")


class WeatherStates(StatesGroup):
    waiting_city = State()


@router.callback_query(F.data == "weather:ask_city")
async def ask_city(cb: CallbackQuery, state: FSMContext):
    await state.set_state(WeatherStates.waiting_city)
    await cb.message.edit_text("Введите название города (например: Алматы).")
    await cb.answer()


@router.message(WeatherStates.waiting_city)
async def city_received(message: Message, state: FSMContext):
    city = message.text.strip()
    await state.clear()
    await message.answer(
        f"Город: <b>{city}</b>\nНажмите, чтобы запросить погоду:",
        reply_markup=weather_city_keyboard(city)
    )


@router.callback_query(F.data.startswith("weather:get:"))
async def get_weather(cb: CallbackQuery):
    user_id = cb.from_user.id
    record(user_id)
    if is_blocked(user_id):
        await cb.answer("Слишком много запросов. Подождите 2 минуты 🙏", show_alert=True)
        return

    _, _, city = cb.data.partition("weather:get:")
    city = city.strip()

    client = WeatherClient()
    try:
        data = await client.get_current(city=city)
        # Пример форматирования ответа
        name = data.get("name", city)
        main = data.get("weather", [{}])[0].get("description", "нет данных")
        temp = data.get("main", {}).get("temp")
        feels = data.get("main", {}).get("feels_like")
        wind = data.get("wind", {}).get("speed")

        text = (
            f"Погода в <b>{name}</b>:\n"
            f"• {main}\n"
            f"• Температура: {temp} °C (ощущается как {feels} °C)\n"
            f"• Ветер: {wind} м/с"
        )

        # Сохранение в MongoDB
        await Mongo.save_weather_request(city=city, payload=data)

        await cb.message.edit_text(text)
        await cb.answer()
    except WeatherError as e:
        await cb.message.edit_text(
            "Не удалось получить погоду. Попробуйте ещё раз.\n"
            f"Причина: {e}"
        )
        await cb.answer()
