import requests
import datetime
import logging
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

logger = logging.getLogger(__name__)
load_dotenv()

BOT_TOKEN = os.getenv('token')
OPEN_WEATHER_TOKEN = os.getenv('open_weather_token')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# словарь эмоджи
EMODJI_DICTIONARY = {
    "Clear": 'Ясно \U00002600',
    "Clouds": 'Облачно \U00002601',
    'Rain': 'Дождливо \U00002614',
    'Drizzle': 'Дождливо \U00002614',
    'Thunder': 'Гроза \U000026A1',
    'Snow': 'Снег \U0001F328',
    'Mist': 'Туман \U0001F32B'
}


def check_tokens() -> bool:
    """проверяем доступность переменных окружения."""
    return all([BOT_TOKEN, OPEN_WEATHER_TOKEN])


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    me = await bot.get_me()
    await message.reply(f'\U0001F916 Привет, {message.from_user.full_name}, '
                        f'меня зовут {me.full_name}, '
                        f'Напиши мне название города и я пришлю погоду')


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q='
            f'{message.text}&appid={OPEN_WEATHER_TOKEN}&units=metric').json()
        city = response['name']
        temperature = response['main']['temp']
        humidity = response['main']['humidity']
        pressure = response['main']['pressure']
        wind_speeed = response['wind']["speed"]
        weather_description = response['weather'][0]['main']
        if weather_description in EMODJI_DICTIONARY:
            emodji = EMODJI_DICTIONARY[weather_description]
        await message.reply(
            f"#####################\n"
            f"По состоянию на "
            f"{datetime.datetime.now().strftime('[%Y-%m-%d] [%H:%M]')}\n"
            f'Погода в городе {city}:\nТемпература: {temperature} '
            f'С° {emodji}\n'
            f'Влажность: {humidity}\nДавление: {pressure} '
            f'мм.рт.ст.\nСкорость ветра: {wind_speeed} м/с\n'
            f'### Хорошего дня! ###\n'
            f"#####################"
        )
    except Exception as error:
        logger.error(error)
        await message.reply('\U00002620 Проверьте город! \U00002620')
    else:
        await message.reply(
            'Посмотри в окно, черт знает, что там происходит...')


if __name__ == '__main__':
    # настройка логирования
    file_handler = logging.FileHandler(
        filename=os.path.join('main.log'))
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers,
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    #######################
    # запуск бота
    if not check_tokens():
        logger.critical('Ошибка, проверьте токены в config.py')
        sys.exit('Ошибка, проверьте токены в config.py')
    executor.start_polling(dp, skip_updates=True)

