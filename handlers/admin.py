from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from DataBase import Sqlite_db
from kyeboards import admin_kb


ID=None

class FSMAdmin(StatesGroup):
	photo = State()
	Name = State()
	description=State()
	price = State()
# проверка на админа
async def make_changes_command(message: types.Message):
	global ID
	ID = message.from_user.id
	await bot.send_message(message.from_user.id, 'Чаво надобно?', reply_markup=admin_kb.button_case_admin)
	await message.delete()



#Загрузка диалога загрузки нового пункта
#@dp.message_handlers(commands='Загрузить', state=none)
async def adm_start(message : types.Message):
	if message.from_user.id == ID:
		await FSMAdmin.photo.set()
		await message.reply('Загрузить фото')


#########EXIT#######
async def cancel_handler(message: types.Message, state: FSMContext):
	if message.from_user.id == ID:
		correct_state = await state.get_state()
		if correct_state is None:
			return
		await state.finish()
		await message.reply('OK')

#Бот ловит фото и записывает в словарь 
#@dp.message_handlers(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state= FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['photo'] = message.photo[0].file_id
		await FSMAdmin.next()
		await message.reply('теперь введи название')

# Бот ловит имя и записывает в словарь
#@dp.message_handlers(state=FSMAdmin.name)
async def load_name(message: types.Message, state= FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['Name'] = message.text
		await FSMAdmin.next()
		await message.reply('теперь введи описание')


#  Бот ловит описание и записывает в словарь
#@dp.message_handlers(state=FSMAdmin.description)
async def load_description(message: types.Message, state= FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['description'] = message.text
		await FSMAdmin.next()
		await message.reply('теперь введи цену. Только цифры')

#  Бот ловит цену и записывает в словарь
#@dp.message_handlers(state=FSMAdmin.price)

async def load_price(message: types.Message, state= FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['price'] = float(message.text)

	await Sqlite_db.sql_add_command(state)			
	await state.finish()



def register_handlers_admin(dp : Dispatcher):
	dp.register_message_handler(adm_start,commands=['Загрузить'], state=None)
	dp.register_message_handler(make_changes_command,commands=['Модератор'], is_chat_admin=True)
	dp.register_message_handler(cancel_handler, state="+", commands='отмена')
	dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="+")
	dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
	dp.register_message_handler(load_name, state=FSMAdmin.Name)
	dp.register_message_handler(load_description,state=FSMAdmin.description)
	dp.register_message_handler(load_price, state=FSMAdmin.price)