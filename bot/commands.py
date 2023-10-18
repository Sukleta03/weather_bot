from aiogram import Dispatcher, types


async def set_default_commands(dp: Dispatcher) -> None:
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start the bot"),
            types.BotCommand("help", "Get help"),
            types.BotCommand('day', "Get weather"),
            types.BotCommand("weather", "Get weather for week"),
            types.BotCommand("about", "About the bot"),
            types.BotCommand("rain", "Will it rain today?"),
            types.BotCommand("subscribe", "Subscribe to weather"),
            types.BotCommand("unsubscribe", "Unsubscribe from weather"),
        ]
    )

