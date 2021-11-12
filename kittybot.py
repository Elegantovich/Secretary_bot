import logging
import os
import requests
import datetime as dt
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv

url_data = {
    'cat': 'https://api.thecatapi.com/v1/images/search',
    'dog': 'https://api.thedogapi.com/v1/images/search',
    'weather': 'http://api.openweathermap.org/data/2.5/'
               'weather?id=498817&appid=41da95281bee035d84f9fbc6b12088c1'
}

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_time(hours):
    if hours in range(6, 12):
        return 'Доброе утро'
    elif hours in range(12, 18):
        return 'Добрый день'
    elif hours in range(18, 23):
        return 'Добрый вечер'
    return 'Доброй ночи'


def get_new_image():
    try:
        response = requests.get(url_data['cat'])
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        print('Произошла ошибка, временно полюбуйтесь собаками')
        response = requests.get(url_data['dog'])
    response = response.json()
    random_animal = response[0].get('url')
    return random_animal


def conv(weather):
    es = ['', 'а', 'ов']
    if weather >= 11 and weather <= 19:
        s = es[2]
    else:
        i = weather % 10
        if i == 1:
            s = es[0]
        elif i in [2, 3, 4]:
            s = es[1]
        else:
            s = es[2]
    return s


def get_new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def weather(update, context):
    chat = update.effective_chat
    response = requests.get(url_data['weather'], params={'units': 'metric'})
    response = response.json()
    weather = response['main'].get('temp')
    speed = response['wind'].get('speed')
    chat = update.effective_chat
    context.bot.send_message(chat.id, text=f'Температура в Санкт-Петребурге '
                             f'{int(weather)} градус{conv(int(weather))}, '
                             f'скорость ветра {round(speed, 1)} м/с')


def wake_up(update, context):
    now = dt.datetime.utcnow()
    period = dt.timedelta(hours=3)
    moscow_moment = now + period
    hours = int(moscow_moment.strftime('%H'))
    now = moscow_moment.strftime('%H:%M')
    day = moscow_moment.strftime('%d.%m.%Y')
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/cats', '/weather'],
                                  ['/start']], resize_keyboard=True)
    response = requests.get(url_data['weather'], params={'units': 'metric'})
    response = response.json()
    weather = round(response['main'].get('temp'), 1)
    speed = response['wind'].get('speed')
    response = (requests.get(url_data['cat'])).json()
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{get_time(hours)}, {name}. Сегодня {day}г., {now}, температура '
             f'воздуха в Санкт-Петербурге {int(weather)} '
             f'градус{conv(int(weather))}, скорость ветра {round(speed, 1)} '
             f'м/с, и да, кстати посмотри какого котика '
             'я тебе нашел ;)',
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())
    context.bot.send_message(
        chat_id=chat.id,
        text='Хочешь получить больше фотогорафий домашних любимцев, '
             'нажми "/cats"',
        reply_markup=button)
    context.bot.send_message(
        chat_id=chat.id,
        text='Хочешь узнать актуальную темепературу воздуха, нажми "/weather"',
        reply_markup=button)


def main():
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('cats', get_new_cat))
    updater.dispatcher.add_handler(CommandHandler('weather', weather))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
