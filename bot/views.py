from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Button, Text
import json

# Create your views here.
import telebot

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


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Salom')
    user = User()
    user.user_id = message.chat.id
    user.save()


@bot.message_handler(content_types='text')
def send_Message(message):
    bot.send_message(message.chat.id, 'Hayrli kun')
