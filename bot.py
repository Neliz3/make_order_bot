import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.handlers import admin, user, callbacks
from app.keyboards import commands

from app.db.engine import create_db, drop_db


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def register_routers():
    dp.include_routers(admin.admin_router, user.user_router, callbacks.callback_router)


async def on_startup():
    await register_routers()
    await bot.set_my_commands(commands.commands)

    # await drop_db()
    await create_db()


async def main():

    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


# TODO: imports (load_env or conf file)
# TODO: create different Schema
# TODO: what is update?
# TODO: all functions (admin too)
# TODO: add user_id into table
# TODO: optimize import
