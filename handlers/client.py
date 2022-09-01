from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext#
from aiogram.dispatcher.filters.state import State, StatesGroup#
from create_bot import dp, bot
from kyeboards import kb_client,First_chat
from aiogram.types import ReplyKeyboardRemove
from DataBase import Sqlite_db
import sqlite3
from aiogram.dispatcher.filters import Text



Chat_id =()
Qest=()



#@dp.message_handler(commands=['start','help'])
async def commands_start(message : types.Message):
	try:
		await bot.send_message(message.from_user.id, 'Добро пожаловать ❗️', reply_markup=kb_client)
		await message.delete()
	except:
		await message.reply(' общение с ботом в ЛС \nhttps://t.me/RegAgentBOT')


#@dp.message_handler(commands=['Правила'])
####################################################################(((((((((())))))))))
async def reg_agent_rule(message : types.Message):
	await bot.send_message(message.from_user.id,'ссылка или текст с правилами')

#@dp.message_handler(commands=['Как_это_работает?'])
####################################################################(((((((((())))))))))
async def reg_agent_howitswork(message : types.Message):
	await bot.send_message(message.from_user.id,'ссылка или текст с примером работы бота и описание идеи')

#=================Переменные


#=========================================Регистрация профиля=================================================
class registration(StatesGroup):
	name = State()
	description = State()
	services = State()
	services1 = State()
	price = State()

#------------------- начало---------------------------

async def reg_start(message : types.Message, state):
	Chat_id = message.chat.id
	await Sqlite_db.sql_First(message,state)
	
	# u=message.chat.id
	# o=sql_First
	# for u in o :
	await message.delete()
	await bot.send_message(message.from_user.id,'Как к вам обращаться?')
	await registration.name.set()
	
	# else:
	# 	await bot.send_message(message.from_user.id, ' Вы уже зарегитрированы ')
	# 	cancel_reg

		


async def cancel_reg(message: types.Message):#, state: FSMContext):
	# correct_state = await state.get_state()
	# if correct_state is None:
		# return
	await bot.send_message(message.from_user.id, ' Вы уже зарегитрированы ')
	await state.reset()



async def reg_agent_name(message : types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
		data['user_ID'] =message.chat.id	
		await registration.next()
		await message.reply('теперь введи описание')


async def reg_agent_description(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data ['description'] = message.text
	await registration.next()
	await bot.send_message(message.from_user.id,'Услуга № 1')


async def reg_agent_services(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data ['services'] = message.text
	await registration.next()
	await bot.send_message(message.from_user.id,'услуга 2')



async def reg_agent_services1(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data ['services1'] = message.text
	await registration.next()
	await bot.send_message(message.from_user.id,'цена например 5.5')	

async def reg_agent_price(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data ['price'] = float=(message.text)
	await registration.next()
	await bot.send_message(message.from_user.id,'Done')

	await Sqlite_db.sql_add_command(state)			
	await state.finish()

# async def drop_reg (message: types.Message, state: FSMContext):
# 	usr=None
# 	if usr is True:
# 		return
# 	await state.finish()
# 	await message.reply('OK')


#==================================ОТМЕНА НОВОРЕГ===============
async def cancel (message: types.Message):
	await bot.send_message(message.from_user.id, ' Вы уже зарегитрированы')
	await bot.send_message(message.from_user.id, ' ну вроде как ')
	await registration.finish()
	



#@dp.message_handler(commands=['Подписка'])
####################################################################(((((((((())))))))))
async def reg_agent_subscribe(message : types.Message):
	await bot.send_message(message.from_user.id,'Подписка', reply_markup=First_chat)


#================================ПОИСК -------- Выводит всю БД::::::::::
async def reg_agent_serch (message: types.Message):
	await Sqlite_db.sql_serch(message)


# # =================================== Запрос на поиск в АНкетах БД  Services======
class FSMSERCH(StatesGroup):
	start_serch = State()
	second_step = State()



async def start_serch (message: types.Message, state : FSMContext):
	await FSMSERCH.start_serch.set()
	await message.delete()	
	await bot.send_message(message.from_user.id,'Какую услугу ищем?\n--- Services----')
	await FSMSERCH.next()
	# await FSMSERCH.start_serch.set()
	
user_id1= ()
async def second_step(message: types.Message, state : FSMContext):
	await bot.send_message(message.from_user.id,'второй шаг')
	user_id1= message.from_user.id
	await bot.send_message(message.from_user.id,' в клиенте')
	await Sqlite_db.sql_serch_services(message,Qest = message.text)
	await state.finish()







def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(commands_start, commands = ['start','help'])
	dp.register_message_handler(reg_agent_rule, commands = ['Правила'])
	dp.register_message_handler(reg_agent_howitswork,Text(equals='Как это работает?', ignore_case=True))
	# dp.register_message_handler(reg_agent_howitswork,commands =['Как это работает?']
	dp.register_message_handler(reg_agent_subscribe,commands =['Подписка'])
	dp.register_message_handler(reg_agent_serch, commands = ('Профиль'))
	dp.register_message_handler(reg_start,commands = ['Регистрация'], state = None)
	dp.register_message_handler(cancel_reg, commands =['Отмена'], state ="*")
	dp.register_message_handler(cancel_reg,Text(equals='отмена', ignore_case=True), state ="*")
	dp.register_message_handler(reg_agent_name,state=registration.name)
	dp.register_message_handler(reg_agent_description, state=registration.description)
	dp.register_message_handler(reg_agent_services, state = registration.services)
	dp.register_message_handler(reg_agent_services1, state = registration.services1)
	dp.register_message_handler(reg_agent_price, state = registration.price)
	dp.register_message_handler(cancel,commands = ['Отмена'], state ="*")
	dp.register_message_handler(start_serch, commands = ['Поиск'])
	dp.register_message_handler(second_step, state= FSMSERCH.second_step)
	# dp.register_message_handler(button,commands=['btn1'])