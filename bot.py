import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats


from app.handlers import admin, user, callbacks, chat
from app.keyboards import commands
from app.db.engine import create_db, drop_db, engine, session_maker

from app.middlewares import db

from conf import TOKEN


dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def register_routers():
    dp.include_routers(chat.chat_router, admin.admin_router, callbacks.callback_router, user.user_router)


async def on_startup():
    await register_routers()
    await bot.set_my_commands(commands.commands, scope=BotCommandScopeAllPrivateChats())

    bot.admins_list = []
    # await drop_db()
    await create_db()


async def on_shutdown():
    #   message to admin about shutdown of a bot
    pass


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(db.database_pool_middleware)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.INFO)
    #   TODO: levels don't work

    asyncio.run(main())


#   TODO: admin part
#   Storage part
