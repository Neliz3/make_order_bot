import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from handlers import user


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


def register_routers(dp: Dispatcher):
    dp.include_router(user.user_router)


async def main():
    dp = Dispatcher()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    register_routers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
