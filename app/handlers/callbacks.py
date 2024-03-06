from aiogram.types import Message
from aiogram import Router


callback_router = Router()


#   Products inline keyboard
@callback_router.callback_query(lambda query: query.data.startswith("a"))
async def products(message: Message):

    await message.answer("!!!!!!!")
