from aiogram.filters import Filter
from aiogram.types import Message


class ChatFilterPrivate(Filter):
    async def __call__(self, message: Message):
        return message.chat.type == "private"


class ChatFilterGroup(Filter):
    async def __call__(self, message: Message):
        return message.chat.type == "group"
