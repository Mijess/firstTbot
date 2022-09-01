import sqlite3 as sq
from create_bot import bot
from handlers import client
from aiogram import executor
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import  InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.types.message import ContentType, ContentTypes


# b11 =InlineKeyboardButton('Начало чаААААта', callback="b11")
# Chat_menu = InlineKeyboardMarkup().add(b11)
# Chat_menu.add(b11)



async def test (message: types.Message):
	await bot.send_message('вот и кнопка',reply_markup=Chat_menu)


def start_chat (message, Qest):
	global base, cur
	base = sq.connect('users.db')
	cur = base.cursor()
	if base:
		print('DataBase_Chat connected\n Enjoy')
	base.execute('CREATE TABLE IF NOT EXISTS Chat_for_two(id TEXT, user_id1 TEXT PRIMARY KEY, user_id2 TEXT PRIMARY KEY)')
	base.commit()

async def chat_for_two(serv2, Qest):

	oy= cur.execute( f"SELECT * FROM chars WHERE user_ID =? ",(serv2,)).fetchall()
	print(oy,'\n\n изменение\n')
	await bot.send_message(f'Результат поиска: \n Имя: {oy[0][0]}\n ID: {oy[0][1]}\n Описание: {oy[0][2]}\n Услуга №1: {oy[0][3]}\n Услуга №2: {oy[0][4]}\n Цена: {oy[0][-1]} ')
	await bot.send_message('Написать?', reply_markup=First_chat)


# @dp.callback_query_handler(commands= "Поиск")
# async def button(message: types.Message):
# 	await bot.send_message(message.from_user.id,"НАжал на кнопку",replay_markup=Chat_menu)