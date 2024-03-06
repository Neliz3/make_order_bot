from typing import Any, Awaitable, Callable, Dict

from aiogram.types import Update
from bot import dp
from app.db import engine


#   Fixture for session in db
@dp.update.outer_middleware()
async def database_pool_middleware(
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
):
    async with engine.session_maker() as session:
        data["session"] = session

        await handler(event, data)
