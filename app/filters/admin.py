from aiogram.filters import Filter
from aiogram.types import Message
from aiogram import Bot


class IsAdmin(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        return message.from_user.id in bot.admins_list
