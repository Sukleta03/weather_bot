from aiogram import types
from bot.loader import bot, dp
from bot.weather import weather_by_city, weather_for_week
from bot.db.models import User
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.loader import session
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.db.queryes import verification
from bot.keyboard import keyboard, city_keyboard
from bot.city import city_list
from loguru import logger

api_key = "7819c42b0c4a4e0ebf0153616230810"


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if await verification(message.from_user.id):
        await bot.send_message(
            message.chat.id, f"Привіт, {message.from_user.first_name}!", reply_markup=keyboard())
    else:
        if message.from_user.first_name != "None":
            name = message.from_user.first_name
        elif message.from_user.username != "None":
            name = message.from_user.username
        elif message.from_user.last_name != "None":
            name = message.from_user.last_name
        else:
            name = ""
        new_user = User(id=message.from_user.id, name=name, city="Чернигов")
        with session() as s:
            s.add(new_user)
            s.commit()
        logger.info(f"New user: {message.from_user.id}")
        await bot.send_message(
            message.chat.id, f"Привіт, {message.from_user.first_name}!", reply_markup=keyboard())


@dp.message_handler(commands=["help"])
async def help(message: types.Message) -> None:
    pass


@dp.message_handler(lambda message: message.text == "Змінити місто")
async def change_city(message: types.Message) -> None:
    await bot.send_message(message.chat.id, "Оберіть місто", reply_markup=city_keyboard(city_list))


@dp.message_handler(lambda message: message.text in city_list)
async def new_city(message: types.Message) -> None:
    city = message.text
    with session() as s:
        user = s.query(User).filter(User.id == message.from_user.id).first()
        user.city = city
        s.commit()
    await bot.send_message(message.chat.id, f"Ви змінили місто на {city}", reply_markup=keyboard())


@dp.message_handler(lambda message: message.text == "Погода на сьогодні")
@dp.message_handler(commands=["day"])
async def day(message: types.Message) -> None:
    city = session.query(User).filter(User.id == message.from_user.id).first().city
    data = await weather_by_city(city, 1)
    text = ''
    for hour in data['forecast']['forecastday'][0]['hour'][8:22]:
        text += f"{hour['time']} | {hour['temp_c']}°C | {hour['condition']['text']}\n"

    await bot.send_message(message.chat.id, text=text)


@dp.message_handler(lambda message: message.text == "Чи буде дощ?")
@dp.message_handler(commands=["rain"])
async def rain(message: types.Message) -> None:
    city = session.query(User).filter(User.id == message.from_user.id).first().city
    data = await weather_by_city(city, 1)

    rain_chance = data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]

    await bot.send_message(message.chat.id,
                           "Сьогодні буде дощ" if rain_chance == 1 else "Сьогодні дощу не буде")


@dp.message_handler(lambda message: message.text == "Погода на тиждень")
@dp.message_handler(commands=["weather"])
async def weather(message: types.Message) -> None:
    city = "Чернигов"
    text = await weather_for_week(city)

    await bot.send_message(message.chat.id, text=text)





