from django.shortcuts import render

__author__ = '@begyy'
from rest_framework.response import Response
from rest_framework.views import  APIView
from .models import User
# Create your views here.
import telebot
bot = telebot.TeleBot('994604539:AAGsEMWEDW93la7rQ5c0JYv62sHiVTu5X1g')

class UpdateBot(APIView):
    def post(self,request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Salom')
    user = User()
    user.user_id = message.chat.id
    user.save()


@bot.message_handler(content_types='text')
def send_Message(message):
    bot.send_message(message.chat.id,'Hayrli kun')

