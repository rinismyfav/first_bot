import telebot
from config import token
from data import Base
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot(token=token)
base = Base()



key1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
key1.row('Погода', 'Новости', '3')

first_menu_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
first_menu_key.row('Погода в Москве', 'Погода в Питере', 'Погода в Комсе')
first_menu_key.row('Назад')

second_menu_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
second_menu_key.row('Новости IT', 'Новости медицины', 'Новости судебных органов РФ')
second_menu_key.row('Назад')

third_menu_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
third_menu_key.row('Время в Москве', 'Время в Питере', 'Время в Комсе')
third_menu_key.row('Назад')


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    if len(base.execute(f'select * from users where tg_id = {chat_id};')) > 0:
        base.execute(f'update users set mode="start" where tg_id={chat_id};')
        bot.send_message(chat_id, 'Рады снова вас видеть.', reply_markup=key1)
    else:
        base.execute(f'insert into users(tg_id, mode) values({chat_id}, "start");')
        bot.send_message(chat_id, 'Добро пожаловать в бота', reply_markup=key1)


@bot.message_handler(content_types=['text'])
def text_processing(message: telebot.types.Message):
    chat_id = message.chat.id
    text = message.text

    user = base.execute(f'select * from users where tg_id={chat_id};')
    if len(user) > 0:
        user = user[0]

        if user['mode'] == 'start':
            if text == 'Погода':
                base.execute(f'update users set mode="mode1" where tg_id={chat_id};')
                bot.send_message(chat_id, 'Вы попали в подменю погоды', reply_markup=first_menu_key)

            if text == 'Новости':
                base.execute(f'update users set mode="mode2" where tg_id={chat_id};')
                bot.send_message(chat_id, 'Вы попали в подменю новостей', reply_markup=second_menu_key)

            if text == 'Время':
                base.execute(f'update users set mode="mode3" where tg_id={chat_id};')
                bot.send_message(chat_id, 'Вы попали в подменю новостей', reply_markup=third_menu_key)

        elif user['mode'] == 'mode1':
            if text == 'Назад':
                base.execute(f'update users set mode="start" where tg_id={chat_id};')
                bot.send_message(chat_id, 'Вы попали в главное меню', reply_markup=key1)

            elif text == 'Погода в Москве':

                url = 'https://meteoinfo.ru/forecasts/russia/moscow-area/moscow'
                response = requests.get(url)

                soup = BeautifulSoup(response.text, "html.parser")
                items = soup.find_all('span', class_='fc_temp_short')

                bot.send_message(chat_id, f'Погода в Москве сегодня: {items[0].text}')

            elif text == 'Погода в Питере':
                url = 'https://meteoinfo.ru/forecasts/russia/leningrad-region/sankt-peterburg'
                response = requests.get(url)

                soup = BeautifulSoup(response.text, "html.parser")
                items = soup.find_all('span', class_='fc_temp_short')

                bot.send_message(chat_id, f'Погода в Питере сегодня: {items[0].text}')

            elif text == 'Погода в Комсе':
                url = 'https://meteoinfo.ru/forecasts/russia/khabarovsk-territory/komsomolsk-na'
                response = requests.get(url)

                soup = BeautifulSoup(response.text, "html.parser")
                items = soup.find_all('span', class_='fc_temp_short')

                bot.send_message(chat_id, f'Погода в Комсе сегодня: {items[0].text}')

        elif user['mode'] == 'mode2':
            if text == 'Назад':
                base.execute(f'update users set mode="start" where tg_id={chat_id};')
                bot.send_message(chat_id, 'Вы попали в главное меню', reply_markup=key1)

            elif text == 'Новости IT':
                url = 'https://3dnews.ru/'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                items = [i.text for i in soup.find_all('li', class_='header')[:5]]
                news = '\n'.join(items)
                bot.send_message(chat_id, f'Новости IT сегодня:\n\n{news}')

            elif text == 'Новости медицины':
                url = 'https://kodeks.ru/news/feed/novosti-mediciny-i-zdravoohraneniya'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                items = [i.text.replace('\n', '').replace('\t', '').strip() for i in soup.find_all('a', class_='news_lst_i_lk news_lk')[21:26]]
                news = '\n'.join(items)
                bot.send_message(chat_id, f'Новости медицины сегодня:\n\n{news}')

            elif text == 'Новости судебных органов РФ':
                url = 'https://kodeks.ru/news/feed/novosti-vysshih-sudebnyh-organov-rf'
                response = requests.get(url)
                print(response)
                soup = BeautifulSoup(response.text, "html.parser")
                items = [i.text.replace('\n', '').replace('\t', '').strip() for i in soup.find_all('a', class_='news_lst_i_lk news_lk')[21:25]]
                news = '\n\n'.join(items)
                bot.send_message(chat_id, f'Новости судебных органов сегодня:\n\n{news}')
                print(f'Новости медицины сегодня:\n\n{news}')

        elif user['mode'] == 'mode3':
            if text == 'Назад':
                base.execute(f'update users set mode="start" where tg_id={chat_id};')
                bot.send_message(chat_id, 'Вы попали в главное меню', reply_markup=key1)

            elif text == 'Время в Москве':


bot.infinity_polling()
