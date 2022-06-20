"""Бот, чтобы поинтересовать, а шо там по погоде в нужном городе."""
import datetime
import logging
import os
import sys

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from api_requests import ask_api
from config import EMODJI_DICTIONARY

logger = logging.getLogger(__name__)
load_dotenv()

BOT_TOKEN = os.getenv('token')
OPEN_WEATHER_TOKEN = os.getenv('open_weather_token')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def check_tokens() -> bool:
    """проверяем доступность переменных окружения."""
    return all([BOT_TOKEN, OPEN_WEATHER_TOKEN])


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Функция реакции на команду /start."""
    me = await bot.get_me()
    await message.reply(f'\U0001F916 Привет, {message.from_user.full_name}, '
                        f'меня зовут {me.full_name}, '
                        f'Напиши мне название города и я пришлю погоду')


@dp.message_handler()
async def get_weather(message: types.Message):
    """Основная логика работы бота."""
    response = ask_api(message.text, OPEN_WEATHER_TOKEN)
    if 'error' in response:
        logger.error(f'Ошибка! {response["error"]}')
        await message.reply(response['message'])
    logger.info(f'статус ответа api {response["code"]}')
    city = response['message']['name']
    temperature = response['message']['main']['temp']
    humidity = response['message']['main']['humidity']
    pressure = response['message']['main']['pressure']
    wind_speeed = response['message']['wind']["speed"]
    weather_description = response['message']['weather'][0]['main']
    if weather_description in EMODJI_DICTIONARY:
        emodji = f'За окном: {EMODJI_DICTIONARY[weather_description]}'
    else:
        emodji = 'Посмотри в окно, черт знает, что там происходит...'
    await message.reply(
        f"#####################\n"
        f"По состоянию на "
        f"{datetime.datetime.now().strftime('[%Y-%m-%d] [%H:%M]')}\n"
        f'Погода в городе {city}:\nТемпература: {temperature} С°\n'
        f'{emodji}\n'
        f'Влажность: {humidity}\nДавление: {pressure} '
        f'мм.рт.ст.\nСкорость ветра: {wind_speeed} м/с\n'
        f'### Хорошего дня! ###\n'
        f"#####################"
    )


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
