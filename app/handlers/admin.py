from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router


admin_router = Router()


#   Enter in role of an admin
@admin_router.message(Command('_admin'))
async def command_start_handler(message: Message):
    await message.answer("admin")


#   See statistics
@admin_router.message(Command('_statistics'))
async def command_start_handler(message: Message):
    await message.answer("statistics")


#   See orders
@admin_router.message(Command('_orders'))
async def command_start_handler(message: Message):
    await message.answer("orders")


#   See, Edit, Add, Del products
@admin_router.message(Command('_products'))
async def command_start_handler(message: Message):
    await message.answer("products")
