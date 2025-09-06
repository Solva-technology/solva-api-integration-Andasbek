import os
import pytest
import asyncio
from aioresponses import aioresponses

from app.services.weather_client import WeatherClient, WeatherError

@pytest.mark.asyncio
async def test_weather_200(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "X")
    client = WeatherClient(base_url="http://example.com")

    with aioresponses() as m:
        m.get("http://example.com/weather", status=200, payload={"name":"Almaty","weather":[{"description":"ясно"}],"main":{"temp":20,"feels_like":19},"wind":{"speed":3}})
        data = await client.get_current("Almaty")
        assert data["name"] == "Almaty"

@pytest.mark.asyncio
async def test_weather_404(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "X")
    client = WeatherClient(base_url="http://example.com")

    with aioresponses() as m:
        m.get("http://example.com/weather", status=404, payload={"cod":404})
        with pytest.raises(WeatherError):
            await client.get_current("NoCity")

@pytest.mark.asyncio
async def test_weather_500(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "X")
    client = WeatherClient(base_url="http://example.com")

    with aioresponses() as m:
        m.get("http://example.com/weather", status=500, payload={"cod":500})
        with pytest.raises(WeatherError):
            await client.get_current("City")

@pytest.mark.asyncio
async def test_weather_timeout(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "X")
    client = WeatherClient(base_url="http://example.com", timeout=0)  # force timeout

    with aioresponses() as m:
        # Simulate timeout by not registering the URL and using a very small timeout
        with pytest.raises(WeatherError):
            await client.get_current("City")
