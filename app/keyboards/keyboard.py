from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.queries import list_products, get_product


class QueryCallback(CallbackData, prefix="query"):
    action: str
    value: int


async def keyboard_choose_product(session: AsyncSession):
    builder = InlineKeyboardBuilder()

    numbers = await list_products(session)

    buttons = (InlineKeyboardButton(
        text=f'{num.id}',
        callback_data=QueryCallback(action="add", value=num.id).pack()) for num in numbers)

    row = builder.row()

    for item in buttons:
        row.add(item)

    return builder.as_markup()


async def keyboard_to_cart():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Amount'),
                KeyboardButton(text='Add to Cart'),
                KeyboardButton(text='/cancel'))
    builder.adjust().as_markup().resize_keyboard = True

    return builder.adjust(2).as_markup()


async def keyboard_choose_amount(session: AsyncSession, id_product, action):
    builder = InlineKeyboardBuilder()

    product = await get_product(session, id_product)

    buttons = (InlineKeyboardButton(
        text=f'{i + 1}',
        callback_data=QueryCallback(action=action, value=i+1).pack()) for i in range(product.amount))

    row = builder.row()

    for item in buttons:
        row.add(item)

    builder.adjust().as_markup().resize_keyboard = True

    return builder.as_markup()


async def keyboard_edit_del():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Edit'),
                KeyboardButton(text='Delete'))

    builder.adjust().as_markup().resize_keyboard = True

    return builder.adjust(2).as_markup()


async def keyboard_approve():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Approve'),
                KeyboardButton(text='Approve All'),
                KeyboardButton(text='Reject'))

    builder.adjust().as_markup().resize_keyboard = True

    return builder.adjust(2).as_markup()


async def keyboard_edit_del_product():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Edit Product'),
                KeyboardButton(text='Delete Product'))

    builder.adjust().as_markup().resize_keyboard = True

    return builder.adjust(2).as_markup()


async def keyboard_purpose():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Business'),
                KeyboardButton(text='Customer'))

    builder.adjust().as_markup().resize_keyboard = True

    return builder.adjust(2).as_markup()
