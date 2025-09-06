from app.keyboards.inline import start_keyboard, weather_city_keyboard, rps_menu_keyboard

def test_start_keyboard_cb():
    kb = start_keyboard()
    data = [b.callback_data for row in kb.inline_keyboard for b in row]
    assert "weather:ask_city" in data
    assert "rps:menu" in data

def test_weather_city_keyboard_format():
    kb = weather_city_keyboard("Алматы")
    cb = kb.inline_keyboard[0][0].callback_data
    assert cb.startswith("weather:get:")
    assert cb.split(":", 2)[-1] == "Алматы"

def test_rps_menu_buttons():
    kb = rps_menu_keyboard()
    data = [b.callback_data for row in kb.inline_keyboard for b in row]
    assert set(data) == {"rps:pick:rock","rps:pick:paper","rps:pick:scissors"}
