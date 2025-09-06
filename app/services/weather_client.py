import os
import asyncio
from typing import Any, Dict, Optional

import aiohttp

class WeatherError(Exception):
    pass

class WeatherClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 7):
        self.base_url = base_url or os.getenv("OPENWEATHER_BASE_URL", "https://api.openweathermap.org/data/2.5")
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.timeout = timeout
    
    async def get_current(self, city: str, lang: str = "ru", units: str = "metric") -> Dict[str, Any]:
        if not self.api_key:
            raise WeatherError("API key is not configured")
        url = f"{self.base_url}/weather"
        params = {"q": city, "lang": lang, "appid": self.api_key, "units": units}
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif 400 <= response.status < 500:
                        raise WeatherError(f"Client error: {response.status}")
                    else:
                        raise WeatherError(f"Server error: {response.status}")
        except asyncio.TimeoutError as e:
            raise WeatherError("Request timed out") from e
        except aiohttp.ClientError as e:
            raise WeatherError(f"Network error: {e}") from e