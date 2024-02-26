from typing import Any, Awaitable, Callable, Dict

from aiogram.types import Update

from bot import dp, bot
from app.db import engine


#   Fixture for session in db
@bot.session.middleware()
async def database_session_middleware(
    handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: Dict[str, Any]
) -> Any:
    async with engine.async_sessionmaker() as session:
        data["session"] = session
        return await handler(event, data)
#
# @bot.session.middleware()
# async def my_middleware(
#     make_request: NextRequestMiddlewareType[TelegramType],
#     bot: "Bot",
#     method: TelegramMethod[TelegramType],
# ) -> Response[TelegramType]:
#     # do something with request
#     return await make_request(bot, method)