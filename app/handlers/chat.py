from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, Bot


chat_router = Router()


#   Add admins
@chat_router.message(Command('admin'))
async def admin_cmd(message: Message, bot: Bot):
    chat_id = message.chat.id

    admins = await bot.get_chat_administrators(chat_id)
    admins = [admin.user.id for admin in admins
              if admin.status == 'administrator' or admin.status == 'creator']

    bot.admins_list = admins

    await message.answer(f"Admins were updated.")
