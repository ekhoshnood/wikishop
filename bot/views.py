from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Button, Text
import requests
import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('994604539:AAGsEMWEDW93la7rQ5c0JYv62sHiVTu5X1g')

class UpdateBot(APIView):
    def post(self, request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


class GetList(APIView):
    def get(self, request):
        data = {'list': []}
        button = Button.objects.all()
        for i in button:
            data['list'].append({'name': i.button})
        return Response(data)


class ButtonText(APIView):
    def post(self, request):
        data = json.loads(request.body)
        try:
            get_button = Button.objects.get(button=data['text'])
            text = Text.objects.get(button=get_button)
            return Response({"text": text.text, "code": 200})
        except:
            return Response({"code": 401})

'''
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'سلام {}'.format(message.from_user.first_name))
    user = User()
    user.user_id = message.chat.id
    user.save()

@bot.message_handler(commands=['هی'])
def hei(message):
    bot.send_message(message.chat.id, 'با هر ردیف کلمه /بعدی را تایپ کنید')
    hei = 0
    if hei==0:
        bot.send_message(message.chat.id, 'شر شر بارون، توی خیابون \n')
    if hei==1:
        bot.send_message(message.chat.id, 'دختره گولم زد، دست به دولم زد \n')
    if hei==2:
        bot.send_message(message.chat.id, 'دولم بزرگ شد، کردم تو کونش \n')
    if hei==3:
        bot.send_message(message.chat.id, 'کونش خون اومد، بردم به دکتر \n')
    if hei==4:
        bot.send_message(message.chat.id, 'دکتر دواش داد، آب انار داد \n')
    if hei==5:
        bot.send_message(message.chat.id, 'امروز خورد، فردا مرد \n')
    if hei==6:
        bot.send_message(message.chat.id, 'مرد دیگه، میخاستی چی بشه؟ \n')
    hei+=1

@bot.message_handler(content_types='text')
def send_Message(message):
    bot.send_message(message.chat.id, 'روی هی/ کلیک کنید')
    if message==0:
        bot.send_message(message.chat.id, 'شر شر بارون، توی خیابون \n')
        bot.send_message(message.chat.id, '/1')
    if message==1:
        bot.send_message(message.chat.id, 'دختره گولم زد، دست به دولم زد \n')
    if message==2:
        bot.send_message(message.chat.id, 'دولم بزرگ شد، کردم تو کونش \n')
    if message==3:
        bot.send_message(message.chat.id, 'کونش خون اومد، بردم به دکتر \n')
    if message==4:
        bot.send_message(message.chat.id, 'دکتر دواش داد، آب انار داد \n')
    if message==5:
        bot.send_message(message.chat.id, 'امروز خورد، فردا مرد \n')
    if message==6:
        bot.send_message(message.chat.id, 'مرد دیگه، میخاستی چی بشه؟ \n')

'''


def Button(message):
    r = requests.get('http://127.0.0.1:8000/api/button')
    data = json.loads(r.text)
    text = 'سلام {}'.format(message.from_user.first_name)
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