from aiogram import types
from loguru import logger
import datetime
from db.models import User
from db.queryes import verification
from .weather import get_weather_for_week, get_weather_by_city_for_date
from .keyboard import main_keyboard, city_keyboard, inline_keyboard_for_subscribe
from .city import city_list, city_to_eng
from .loader import bot, session, dp


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if await verification(message.from_user.id):
        await bot.send_message(
            message.chat.id,
            f"Привіт, {message.from_user.first_name}!",
            reply_markup=main_keyboard()
        )
    else:
        name = message.from_user.first_name \
               or message.from_user.username \
               or message.from_user.last_name \
               or ""
        new_user = User(id=message.from_user.id, name=name, city="Kivy", subscribe=True)
        with session() as s:
            s.add(new_user)
            s.commit()
            logger.info(f"New user: {message.from_user.id}")
        await bot.send_message(
            message.chat.id,
            f"Привіт, {message.from_user.first_name}!")
        await change_city(message)


@dp.message_handler(lambda message: message.text in city_list)
async def new_city(message: types.Message) -> None:
    city = city_to_eng.get(message.text)
    with session() as s:
        user = s.query(User).filter(User.id == message.from_user.id).first()
        if user:
            user.city = city
            s.commit()
    await bot.send_message(
        message.chat.id,
        f"Ви змінили місто на {message.text}",
        reply_markup=main_keyboard()
    )


@dp.message_handler(commands=["help"])
async def help(message: types.Message) -> None:
    await bot.send_message(
        message.chat.id,
        f"Введіть /start для початку роботи з ботом\n"
        f"Введіть /weather для отримання погоди зараз\n"
        f"Введіть /day для отримання погоди на сьогодні\n"
        f"Введіть /rain для перевірки чи буде дощ\n"
        f"Введіть /weather_for_week для отримання погоди на тиждень\n"
        f"Введіть /subscribe для підписки на розсилку\n"
        f"Введіть /unsubscribe для відписки від розсилки\n"
        f"Введіть /about для отримання інформації про бота\n"
        f"Введіть /help для отримання довідки\n"
    )


@dp.message_handler(lambda message: message.text == "Змінити місто")
async def change_city(message: types.Message) -> None:
    await bot.send_message(message.chat.id, "Оберіть місто", reply_markup=city_keyboard(city_list))


@dp.message_handler(commands=["weather"])
@dp.message_handler(lambda message: message.text == "Погода зараз")
async def weather(message: types.Message) -> None:
    city = session.query(User).filter(User.id == message.from_user.id).first().city
    data = await get_weather_by_city_for_date(city, datetime.date.today())

    await bot.send_message(message.chat.id, text=data['current']['condition']['text'] + '\n'
                                                 + f"Температура: {data['current']['temp_c']}°C\n")


@dp.message_handler(lambda message: message.text == "Погода на сьогодні")
@dp.message_handler(commands=["day"])
async def day(message: types.Message) -> None:
    city = session.query(User).filter(User.id == message.from_user.id).first().city
    data = await get_weather_by_city_for_date(city, datetime.date.today())
    text = ''
    for hour in data['forecast']['forecastday'][0]['hour'][8:22]:
        text += f"{hour['time']} | {hour['temp_c']}°C | {hour['condition']['text']}\n"

    await bot.send_message(message.chat.id, text=text)


@dp.message_handler(lambda message: message.text == "Чи буде дощ?")
@dp.message_handler(commands=["rain"])
async def rain(message: types.Message) -> None:
    city = session.query(User).filter(User.id == message.from_user.id).first().city
    data = await get_weather_by_city_for_date(city, datetime.date.today())
    will_it_rain = data["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"]

    await bot.send_message(message.chat.id,
                           "Сьогодні буде дощ" if will_it_rain == 1 else "Сьогодні дощу не буде")


@dp.message_handler(lambda message: message.text == "Погода на тиждень")
@dp.message_handler(commands=["weather_for_day"])
async def weather_for_week(message: types.Message) -> None:
    city = session.query(User).filter(User.id == message.from_user.id).first().city
    text = await get_weather_for_week(city)

    await bot.send_message(message.chat.id, text=text)


async def subscribe(message: types.Message) -> None:
    with session() as s:
        user = s.query(User).filter(User.id == message.from_user.id).first()
        if user:
            user.subscribe = True
            s.commit()
    await bot.send_message(
        message.chat.id,
        f"Ви підписались на розсилку",
        reply_markup=main_keyboard()
    )


async def unsubscribe(message: types.Message) -> None:
    with session() as s:
        user = s.query(User).filter(User.id == message.from_user.id).first()
        if user:
            user.subscribe = False
            s.commit()
    await bot.send_message(
        message.chat.id,
        f"Ви відписались від розсилки",
        reply_markup=main_keyboard()
    )


@dp.message_handler()
async def unknown_message(message: types.Message) -> None:
    await bot.send_message(message.chat.id, "Я не знаю такої команди 😔")
    await bot.send_message(message.chat.id, "Введіть /help для довідки", reply_markup=main_keyboard())


async def send_weather_to_subscribers() -> None:
    with session() as s:
        users = s.query(User).filter(User.subscribe == True).all()

        for user in users:
            date = datetime.date.today() + datetime.timedelta(days=1)
            data = await get_weather_by_city_for_date(user.city, date)
            await bot.send_message(user.id,
                                   f"Погода на завтра:\n"
                                   f"Максимальна температура: {data['forecast']['forecastday'][0]['day']['maxtemp_c']}°C\n"
                                   f"Мінімальна температура: {data['forecast']['forecastday'][0]['day']['mintemp_c']}°C\n"
                                   f"Опади: {data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']}%\n",
                                   reply_markup=inline_keyboard_for_subscribe()
                                   )
        logger.info(f"Weather sent, to {len(users)} users, at {datetime.datetime.now()}")