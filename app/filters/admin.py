from aiogram import Bot
from aiogram.filters import Filter
from aiogram.types import Message


class IsAdmin(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        return message.from_user.id in bot.admin_list
