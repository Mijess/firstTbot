from aiogram.utils import executor
from create_bot import dp, bot
from DataBase import Sqlite_db



async def on_startup(_):
	print('Бот сейчас online\n!!!!!!!!!!!!!!!!!!!')
	Sqlite_db.sql_start()

from handlers import client, admin#, other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)



executor.start_polling(dp, skip_updates=True, on_startup = on_startup)
