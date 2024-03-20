import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.handlers import admin, user, callbacks, chat
from app.db.engine import create_db, drop_db
from app.middlewares import db

from conf import TOKEN, description


dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def register_routers():
    dp.include_routers(chat.chat_router, admin.admin_router,
                       callbacks.callback_router, user.user_router)


async def on_startup():
    bot.admin_list = []

    await bot.delete_my_commands()
    await register_routers()

    # await drop_db()
    await create_db()


async def on_shutdown():
    logging.critical("Bot shut down!")


async def main():
    await bot.set_my_description(description)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(db.database_pool_middleware)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.INFO)

    asyncio.run(main())
