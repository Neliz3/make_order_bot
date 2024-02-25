from typing import Any, Awaitable, Callable, Dict

from aiogram.types import Update

from bot import dp
from app.db import engine


#   Fixture for session in db
@dp.update.outer_middleware()
async def database_session_middleware(
    handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: Dict[str, Any]
) -> Any:
    async with engine.async_sessionmaker() as session:
        data["session"] = session
        return await handler(event, data)
