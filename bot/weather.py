import aiohttp
import asyncio
import datetime
import locale
import os

locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
# api_key = str(os.getenv("API_KEY"))
api_key = "7819c42b0c4a4e0ebf0153616230810"

async def weather_by_city(city: str, days: int):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.weatherapi.com/v1/forecast.json?" \
              f"key={api_key}" \
              f"&q={city}" \
              f"&days={days}" \
              f"&lang=uk"

        async with session.get(url) as resp:
            data = await resp.json()
    return data


async def weather_history(city: str, days: int):
    async with aiohttp.ClientSession() as session:
        date = datetime.date.today() - datetime.timedelta(days=days)
        end_date = datetime.date.today()
        url = f"https://api.weatherapi.com/v1/history.json?" \
              f"key={api_key}" \
              f"&q={city}" \
              f"&dt={date}" \
              f"&end_dt={end_date}" \
              f"&lang=uk"

        async with session.get(url) as resp:
            data = await resp.json()

        return data


async def weather_for_week(city: str):
    week_day = datetime.date.weekday(datetime.date.today())
    days = 7 - week_day
    history_weather = await weather_history(city, days)
    future_weather = await weather_by_city(city, days)
    result = []

    for i in history_weather["forecast"]["forecastday"][:-1]:
        day = datetime.datetime.strptime(i['date'], '%Y-%m-%d').strftime('%A').capitalize()
        condition = i['day']['condition']['text']
        temp_range = f"{i['day']['mintemp_c']}-{i['day']['maxtemp_c']}°C"
        row = f"{day.ljust(12)} | {condition.ljust(20)} | {temp_range}"
        result.append(row)

    for i in future_weather["forecast"]["forecastday"]:
        day = datetime.datetime.strptime(i['date'], '%Y-%m-%d').strftime('%A').capitalize()
        condition = i['day']['condition']['text']
        temp_range = f"{i['day']['mintemp_c']}-{i['day']['maxtemp_c']}°C"
        row = f"{day.ljust(12)} | {condition.ljust(20)} | {temp_range}"
        result.append(row)

    return '\n'.join(result)


# print(asyncio.run(weather_for_week("Чернигов")))



