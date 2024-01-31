from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Погода на сьогодні"),
                KeyboardButton(text="Погода зараз"),
            ],
            [
                KeyboardButton(text="Чи буде дощ?"),
                KeyboardButton(text="Змінити місто"),
            ],
        ],
        resize_keyboard=True
    )


def city_keyboard(city_list, columns=2):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=columns)

    city_lists = [city_list[i:i + columns] for i in range(0, len(city_list), columns)]

    for cities in city_lists:
        keyboard.add(*[KeyboardButton(text=city) for city in cities])

    return keyboard


def inline_keyboard_for_subscribe():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Відписатися", callback_data="unsubscribe"),
            ]
        ]
    )
