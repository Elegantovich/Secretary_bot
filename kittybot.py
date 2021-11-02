import logging
import os
import requests
import datetime as dt 

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters

from dotenv import load_dotenv 

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


URL = 'https://api.thecatapi.com/v1/images/search'
nasa_url = 'https://api.nasa.gov/planetary/apod?api_key=WLJ4nXKANWPDukAtRWCAhhckxfE6LI5nk9OjxKmA'
nasa_key = 'WLJ4nXKANWPDukAtRWCAhhckxfE6LI5nk9OjxKmA'

'Account_ID:4b87d67e-8e32-4e7b-bf9a-9943b6d4032e'


def time(hours):
    if hours > 6 and hours <= 11:
        return 'Доброе утро'
    elif hours > 12 and hours <= 17:
        return 'Добрый день'
    elif hours >= 18 and hours <= 21:
        return 'Добрый вечер'
    elif hours >= 22:
        return 'Доброй ночи'


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_new_imagecosmos():

    response = requests.get(nasa_url)
    response = response.json()
    cosmos = response.get('hdurl')
    return cosmos


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def nasa(update, context):
    chat = update.effective_chat
    response = requests.get(nasa_url)
    response = response.json()
    author = response.get('copyright')
    if not author:
        author = 'Неизвестен'
    name = response.get('title')
    description = response.get('explanation')
    context.bot.send_message(chat.id, text=f'Автор "{author}", название "{name}"')
    response = requests.get(nasa_url)
    context.bot.send_photo(chat.id,  get_new_imagecosmos())
    context.bot.send_message(chat.id,  text=f'Описание "{description}".')


def weather(update, context):
    chat = update.effective_chat
    new_url = 'http://api.openweathermap.org/data/2.5/weather?id=498817&appid=41da95281bee035d84f9fbc6b12088c1'
    responses = requests.get(new_url, params={'units': 'metric'})
    responses = responses.json()
    weather = responses['main'].get('temp')
    speed = responses['wind'].get('speed')
    chat = update.effective_chat
    context.bot.send_message(chat.id, text=f'Температура в Санкт-Петребурге {weather} градусов, скорость ветра {speed} м/с')


def wake_up(update, context):
    print(update)
    now = dt.datetime.utcnow()
    period = dt.timedelta(hours=3)
    moscow_moment = now + period
    hours = int(moscow_moment.strftime('%H'))
    now = moscow_moment.strftime('%H:%M')
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/cats', '/weather'], 
                                  ['Космос', '/start']], resize_keyboard=True)
    weath = 'http://api.openweathermap.org/data/2.5/weather?id=498817&appid=41da95281bee035d84f9fbc6b12088c1'
    responsed = requests.get(weath, params={'units': 'metric'})
    responsed = responsed.json()
    weather = round(responsed['main'].get('temp'), 1)
    speed = responsed['wind'].get('speed')
    response = requests.get(URL)
    response = response.json()
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{time(hours)}, {name}. Сейчас {now}, температура воздуха в Санкт-Петербурге {weather} градуса, скорость ветра {speed} м/с, рекомендую одеться потеплее и кстати посмотри какого котика я тебе нашел',
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())
    context.bot.send_message(
        chat_id=chat.id,
        text='Хочешь получить больше котиков, нажми "Котики"',
        reply_markup=button)
    context.bot.send_message(
        chat_id=chat.id,
        text='Хочешь узнать темепературу воздуха, нажми "Погода"',
        reply_markup=button)
    context.bot.send_message(
        chat_id=chat.id,
        text='Хочешь увидеть фотки космоса, нажми "Космос"',
        reply_markup=button
    )


def main():
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('cats', new_cat))
    updater.dispatcher.add_handler(CommandHandler('weather', weather))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, nasa))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main() 