import sqlite3 as sq
from create_bot import bot
from handlers import client
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import itertools 


def sql_start():
	global base, cur
	base = sq.connect('users.db')
	cur = base.cursor()
	if base:
		print('DataBase connected\n Enjoy')
	base.execute('CREATE TABLE IF NOT EXISTS chars(services1 TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT, services TEXT, user_ID TEXT)')
	base.commit()


async def sql_add_command(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO chars VALUES (?,?,?,?,?,?)', tuple(data.values()))
		base.commit()

#-------------------------------------Проверка на повторную регистрацию ---------------------
async def sql_First(message,Chat_id):
	from handlers.client import Chat_id
	Chat_id = message.chat.id
	
	#await bot.send_message(message.from_user.id,'' )
	#result=cur.fetchall()
	for ret in cur.execute(f'SELECT user_ID FROM chars WHERE user_ID = {Chat_id}',).fetchall():
		if ret == Chat_id:
		#await bot.send_message(message.from_user.id, f'{result[0]}')
			await bot.send_message(message.from_user.id,'Регистрация нового профиля')
			return
		else:
			await bot.send_message(message.from_user.id,'eлсе')
			await client.cancel(message)

	


#-----------------------Поиск уникального ID Телеги в БД, ID Отличается  в группе и в ЛС----------

async def sql_serch(message):
	from handlers.client import Chat_id
	Chat_id = message.chat.id
	for ret in cur.execute(f'SELECT * FROM chars WHERE user_ID = {Chat_id}',).fetchall():
		await bot.send_message(message.from_user.id, f' Имя: {ret[0]}\n Описание: {ret[2]}\n Услуга №1: {ret[4]}\n Услуга №2 {ret[5]} \n Цена:{ret[-1]}')
	 
	
		
#---------------------- Вывод введных данных в профиль--------------------
async def sql_read(message):
	for ret in cur.execute('SELECT * FROM chars').fetchall():
		await bot.send_message(message.from_user.id, f' Имя: {ret[0]}\n Описание: {ret[1]}\n Услуга №1: {ret[2]}\n Услуга №2 {ret[3]} \n Цена:{ret[-1]}')

# +++++++++++++++++++==============ПОИСК В БД АНКЕТ по Services============+++++++++++++++++


# Fuzz.WRatio



async def sql_serch_services(message, Qest):
	from handlers.client import Qest
	Qest = message.text
	await bot.send_message(message.from_user.id,'Уже в SQL ПОшел')
	# print ( f'SELECT services FROM chars WHERE services LIKE ? {Qest}' )
	Try= cur.execute( f"SELECT * FROM chars",).fetchall()
	rez= (process.extract ((Qest),(Try)))
	REsult =list(rez[0])
	serv1= REsult[0][0]
	serv2=REsult[0][1]
	print (serv2)
	print(serv1,'\n',serv2,'\n в сйлдб')
	await Chat.chat_for_two(serv2,)







# ================================================= v0.1===================Выдача services  и  services 1 
# async def sql_serch_services(message, Qest):
# 	from handlers.client import Qest
# 	Qest = message.text
# 	await bot.send_message(message.from_user.id,'Уже в SQL ПОшел')
# 	# print ( f'SELECT services FROM chars WHERE services LIKE ? {Qest}' )
# 	Try= cur.execute( f"SELECT services,services1 FROM chars",).fetchall()
# 	rez= (process.extract ((Qest),(Try)))
# 	REsult =list(rez[0])
# 	serv1= REsult[0][0]
# 	serv2=REsult[0][1]
# 	print(serv1,'\n',serv2,'\n', Try)
# 	cur.execute( "SELECT user_ID FROM chars WHERE services = ?",(serv2,)).fetchall()
# 	# print (cur.execute.fetchone())
# =================================================
	

	# print (rez.index(60) in rez[0])
	# print (f'rez{query}')
	# -------В ПЕРВОМ СПИСКЕ ВТРОЕ ЗНАЧЕНИЕ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	# if rez[0][1] >80:
		# print(f' Имя: {rez[0][2]}\n \n{rez[1]}\n \n  Описание: {rez[1]}\n \n Услуга №1: {rez[2]}\n \n Услуга №2 {rez[3]} \n \n Цена:{rez[-1]}')
	# await bot.send_message(message.from_user.id, f' Имя: {rez[0]}\n \n{rez[1]}\n \n  Описание: {rez[1]}\n \n Услуга №1: {rez[2]}\n \n Услуга №2 {rez[3]} \n \n Цена:{rez[-1]}')
		


# async def sql_serch_services(message, Qest):
# 	from handlers.client import Qest
# 	Qest = message.text
# 	print (type(Qest))
# 	await bot.send_message(message.from_user.id,'Уже в SQL ПОшел')
# 	# print ( f'SELECT services FROM chars WHERE services LIKE ? {Qest}' )
# 	for ret in cur.execute( f"SELECT * FROM chars WHERE services=? ",(Qest,),).fetchall():
# 		await bot.send_message(message.from_user.id,'Уже в SQL после списка')
# 		print (ret)
# 		if not ret == Qest:
# 			await bot.send_message(message.from_user.id, 'Совпадения')
# 			await bot.send_message(message.from_user.id, f'Имя: {ret[0]}\nОписание: {ret[1]}\nУслуга №1: {ret[2]}\nУслуга №2 {ret[3]} \n Цена:{ret[-1]}')
# 		else:
			
# 			await bot.send_message(message.from_user.id, "Не найдено")






