from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Погода", callback_data="weather:ask_city")],
        [InlineKeyboardButton(text="Камень-Ножницы-Бумага", callback_data="rps:menu")],
    ])

def weather_city_keyboard(city: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Показать погду для {city}", callback_data=f"weather:get:{city}")],
    ])

def rps_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Камень", callback_data="rps:pick:rock")],
        [InlineKeyboardButton(text="Ножницы", callback_data="rps:pick:scissors")],
        [InlineKeyboardButton(text="Бумага", callback_data="rps:pick:paper")],
    ])

def rps_again_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сыграть ещё", callback_data="rps:menu")],
    ])