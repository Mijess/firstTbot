from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import  InlineKeyboardMarkup,InlineKeyboardButton

b1 = KeyboardButton('/Правила')
b2 = KeyboardButton('Как это работает?')
b3 = KeyboardButton('/Подписка')
b4 = KeyboardButton('/start')
reg = KeyboardButton('/Регистрация') 
Profile = KeyboardButton('/ПРОФИЛЬ')
Serch = KeyboardButton ('/Поиск')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
#one_time_keyboard=True - прячет клаву после нажатия
kb_client.add(b1).add(b2).add(b3).insert(b4).add(reg).add(Profile).add(Serch)



button_first=InlineKeyboardButton("Кнопка",callback_data='but_first')
First_chat = InlineKeyboardMarkup().add(button_first)