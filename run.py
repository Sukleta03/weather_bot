from aiogram import Dispatcher
from aiogram.utils import executor
from loguru import logger
from bot.loader import engine, Base, dp


async def start(dp: Dispatcher) -> None:
    Base.metadata.create_all(engine)
    # await set_default_commands(dp)
    # scheduler.add_job(send_weather_to_subscribers, 'cron', hour=20, minute=0)
    # scheduler.start()
    logger.info("bot started")


async def shutdown(dp: Dispatcher) -> None:
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info("bot finished")


if __name__ == "__main__":
    logger.add(
        "bot/logs/debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="30 KB",
        compression="zip",
    )
    executor.start_polling(dp, skip_updates=True, on_startup=start, on_shutdown=shutdown)