from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Погода на сьогодні"),
                KeyboardButton(text="Погода на тиждень")
            ],
            [
                KeyboardButton(text="Чи буде дощ?"),
                KeyboardButton(text="Змінити місто"),
            ],
        ],
        resize_keyboard=True
    )



def city_keyboard(city_list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for city in city_list:
        keyboard.add(KeyboardButton(text=city))
    return keyboard