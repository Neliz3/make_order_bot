import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.handlers import admin, user, callbacks
from app.keyboards import commands
from app.db.engine import create_db, drop_db, engine

from conf import TOKEN


dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def register_routers():
    dp.include_routers(admin.admin_router, user.user_router, callbacks.callback_router)


async def on_startup():
    await register_routers()
    await bot.set_my_commands(commands.commands)

    # await drop_db()
    await create_db()


async def on_shutdown():
    #   message to admin about shutdown of a bot
    await engine.dispose()


async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.INFO)
    asyncio.run(main())


# TODO: create different Schema
# TODO: all functions (admin too)
# TODO: add user_id into table
# TODO: optimize import
