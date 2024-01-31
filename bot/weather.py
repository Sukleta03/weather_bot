import aiohttp
import datetime
import locale
import os

try:
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C')

api_key = str(os.getenv("API_KEY"))


async def get_weather_by_city_for_date(city: str, data):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.weatherapi.com/v1/forecast.json?" \
              f"key={api_key}" \
              f"&q={city}" \
              f"&dt={data}" \
              f"&lang=uk"

        async with session.get(url) as resp:
            data = await resp.json()
    return data


async def get_weather_by_city_for_future_days(city: str, days: int):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.weatherapi.com/v1/forecast.json?" \
              f"key={api_key}" \
              f"&q={city}" \
              f"&days={days}" \
              f"&lang=uk"

        async with session.get(url) as resp:
            data = await resp.json()
    return data


async def get_weather_by_city_for_last_days(city: str, days: int):
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


async def get_weather_for_week(city: str):
    week_day = datetime.date.weekday(datetime.date.today())
    history_weather = await get_weather_by_city_for_last_days(city, week_day)
    future_weather = await get_weather_by_city_for_future_days(city, 7 - week_day)
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
