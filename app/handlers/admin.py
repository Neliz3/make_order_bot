from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router


admin_router = Router()


@admin_router.message(Command('statistic'))
async def command_start_handler(message: Message):
    await message.answer("statistic")


@admin_router.message(Command('orders'))
async def command_start_handler(message: Message):
    await message.answer("orders")
