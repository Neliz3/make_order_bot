from aiogram.types import Message
from aiogram import Router


from app.db.engine import session_maker

from app.db.queries import add_user

callback_router = Router()


#   Products inline keyboard
@callback_router.callback_query(lambda query: query.data.startswith("a"))
async def products(message: Message):
    user = message.from_user
    await add_user(session_maker(), first_name=user.first_name, last_name='', address='', phone='')

    await message.answer("!!!!!!!")
