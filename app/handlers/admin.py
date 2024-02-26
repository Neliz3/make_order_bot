from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from app.filters import admin

from app.db.engine import session_maker

from app.db.queries import list_users

admin_router = Router()
admin_router.message.filter(admin.IsAdmin())


#   Enter in role of an admin
@admin_router.message(Command('admin'))
async def command_start_handler(message: Message):
    await message.answer("admin")


#   See statistics
@admin_router.message(Command('statistics'))
async def command_start_handler(message: Message):
    result = await list_users(session_maker())
    for user in result:
        await message.answer(f"{user.first_name}")


#   See orders
@admin_router.message(Command('orders'))
async def command_start_handler(message: Message):
    await message.answer("orders")


#   See, Edit, Add, Delete products
@admin_router.message(Command('products'))
async def command_start_handler(message: Message):
    await message.answer("products")
