from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.filters import Command
from aiogram import Router


user_router = Router()


#   Register, Send the instruction
@user_router.message(Command('start'))
async def command_start_handler(message: Message):
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


#   Change amount, Delete, Approve
@user_router.message(Command('view_cart'))
async def command_start_handler(message: Message):
    await message.answer("cart")


#   See products, Add to cart, Choose amount
@user_router.message(Command('products'))
async def command_start_handler(message: Message):
    await message.answer("products")


#   Send instruction
@user_router.message(Command('help'))
async def command_start_handler(message: Message):
    await message.answer("products")


#   Unrecognized messages
@user_router.message()
async def command_echo_handler(message: Message):
    await message.answer(f"Dear, {message.from_user.full_name}, I do not understand you. Try again, please )")


