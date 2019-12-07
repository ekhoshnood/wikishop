'''
import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('994604539:AAGsEMWEDW93la7rQ5c0JYv62sHiVTu5X1g')


def Button(message):
    r = requests.get('http://127.0.0.1:8000/api/button')
    data = json.loads(r.text)
    text = 'salam aleikom {}'.format(message.from_user.first_name)
    key = ReplyKeyboardMarkup(True, False)

    for i in range(len(data['list'])):
        button = KeyboardButton(data['list'][i]['name'])
        key.add(button)
    bot.send_message(message.from_user.id, text, reply_markup=key)


@bot.message_handler(commands=['start'])
def start(message):
    Button(message)

@bot.message_handler(content_types='text')
def send_message(message):
    link = 'http://127.0.0.1:8000/api/text'
    text = {"text":message.text}
    r = requests.post(link, data=json.dumps(text))
    data = json.loads(r.text)

    if data['code'] == 401:
        bot.send_message(message.from_user.id, 'sorry {} some tokhmi takhayoli problem'.format(message.from_user.first_name))
    else:
        wiki = data['text']
        bot.send_message(message.from_user.id, wiki)


bot.polling()
'''