import requests


def ask_api(text, opt):
    return requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={text}'
        f'&appid={opt}&units=metric').json()
