from aiogram.filters import Filter
from aiogram.types import Message


class ChatFilter(Filter):
    async def __call__(self, message: Message):
        return message.chat.type == "private"
