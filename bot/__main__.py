from bot.loader import dp
from loguru import logger
from aiogram.utils import executor
from bot.commands import set_default_commands
from aiogram import Dispatcher
from bot.loader import engine, Base


async def start(dp: Dispatcher) -> None:
    Base.metadata.create_all(engine)
    await set_default_commands(dp)
    logger.info("bot started")


async def shutdown(dp: Dispatcher) -> None:

    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info("bot finished")


if __name__ == "__main__":
    logger.add(
        "logs/debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="30 KB",
        compression="zip",
    )
    executor.start_polling(dp, skip_updates=True, on_startup=start, on_shutdown=shutdown)