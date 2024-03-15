import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.handlers import admin, user, callbacks, chat
from app.db.engine import create_db, drop_db

from app.middlewares import db

from conf import TOKEN


dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
bot.admins_list = []

async def register_routers():
    dp.include_routers(chat.chat_router, admin.admin_router, callbacks.callback_router, user.user_router)


async def on_startup():
    await register_routers()
    bot.admins_list = []

    # await drop_db()
    await create_db()


async def on_shutdown():
    logging.critical("Bot shut down!")


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

    # TODO: indexing

    asyncio.run(main())

#   Storage part
