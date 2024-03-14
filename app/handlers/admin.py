from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Dict, Any

from app.filters import admin

from app.db.queries import list_users, add_product

admin_router = Router()
admin_router.message.filter(admin.IsAdmin())


#   Enter in role of an admin
@admin_router.message(Command('admin_'))
async def admin_cmd(message: Message):
    await message.answer("admin")


#   See statistics
@admin_router.message(Command('statistics_'))
async def statistics_cmd(message: Message, session: AsyncSession):
    result = await list_users(session)
    for user in result:
        await message.answer(f"{user.first_name}")


#   See orders
@admin_router.message(Command('orders_'))
async def orders_cmd(message: Message):
    await message.answer("orders")


#   See, Edit, Add, Delete products
class ProductsAdd(StatesGroup):
    title = State()
    price = State()
    amount = State()


@admin_router.message(Command('products_'))
async def products_cmd(message: Message, state: FSMContext):
    await state.set_state(ProductsAdd.title)
    await message.answer("Enter a product title")


@admin_router.message(ProductsAdd.title)
async def process_first_name(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(ProductsAdd.price)
    await message.answer("Enter a product price")


@admin_router.message(ProductsAdd.price)
async def process_last_name(message: Message, state: FSMContext) -> None:
    await state.update_data(price=message.text)
    await state.set_state(ProductsAdd.amount)
    await message.answer("Enter a product amount")


@admin_router.message(ProductsAdd.amount)
async def process_phone(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(amount=message.text)

    data = await state.get_data()
    await state.clear()

    await add_to_database(message, data, session=session)


async def add_to_database(message: Message, data: Dict[str, Any], session):
    title = data["title"]
    price = int(data["price"])
    amount = int(data["amount"])

    await add_product(session,
                      title=title,
                      price=price,
                      amount=amount)

    answer = f"{title} {price} ({amount}) was added"
    await message.answer(text=answer)
