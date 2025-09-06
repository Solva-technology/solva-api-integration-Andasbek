# app/main.py
import asyncio
import logging
import os
import contextlib

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties  # <-- добавь импорт

from app.handlers.start import router as start_router
from app.handlers.weather import router as weather_router
from app.handlers.rps import router as rps_router
from app.services.sessions import periodic_cleanup_sessions
from app.utils.logging import setup_logging


async def main() -> None:
    setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))
    logger = logging.getLogger("app")

    # важно: используем os.environ[...] чтобы упасть явно, если переменная не задана
    bot = Bot(
        token=os.environ["BOT_TOKEN"],
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),  # <-- вот так
    )
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(weather_router)
    dp.include_router(rps_router)

    cleanup_task = asyncio.create_task(periodic_cleanup_sessions(interval_sec=120))

    logger.info("Bot starting ...")
    try:
        await dp.start_polling(bot)
    finally:
        cleanup_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await cleanup_task


if __name__ == "__main__":
    asyncio.run(main())
