from django.urls import path
from .views import UpdateBot, GetList, ButtonText
app_name = 'bot'
urlpatterns = [
    path('telegram', UpdateBot.as_view(), name='update'),
    path('button', GetList.as_view(), name='button-list'),
    path('text', ButtonText.as_view(), name='text'),
]

