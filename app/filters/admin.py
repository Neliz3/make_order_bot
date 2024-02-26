from aiogram.filters import Filter
from aiogram.types import Message
from conf import ADMIN


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.first_name in ADMIN

# TODO: make checking through an id
