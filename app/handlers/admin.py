from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.utils.markdown import hstrikethrough

from sqlalchemy.ext.asyncio import AsyncSession

from prettytable import PrettyTable

from typing import Dict, Any

from app.filters import admin
from app.keyboards.keyboard import keyboard_approve

from app.db.queries import (list_users,
                            add_product, list_carts, list_products, get_product, get_cart,
                            update_cart, delete_cart)
import bot

admin_router = Router()
admin_router.message.filter(admin.IsAdmin())


#   Enter in role of an admin
@admin_router.message(Command('admin_'))
async def admin_cmd(message: Message):
    await message.answer("admin")


@admin_router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Cancelled.", reply_markup=ReplyKeyboardRemove())


#   See statistics
@admin_router.message(Command('statistics_'))
async def statistics_cmd(message: Message, session: AsyncSession):
    result = await list_users(session)
    for user in result:
        await message.answer(f"{user.first_name}")


#   See orders
@admin_router.message(Command('_orders'))
async def orders_cmd(message: Message, session: AsyncSession):
    table = PrettyTable()

    table.title = "Orders"

    table.field_names = ['#', 'Product', 'Amount', 'Total', 'Approval']

    carts = await list_carts(session=session)
    for cart in carts:
        product = await get_product(session, cart.id_product)
        table.add_row([f'{cart.id}',
                       f'{product.title}',
                       f'{cart.amount}',
                       f'{cart.amount * product.price}',
                       f'{cart.approval}'])

    text = f'`{table.get_string()}`'

    await message.answer(text, parse_mode='Markdown', reply_markup=await keyboard_approve())


@admin_router.message(F.text == "Approve All")
async def approve_all_process(message: Message, session: AsyncSession):
    carts = await list_carts(session=session)
    for cart in carts:
        await update_cart(session, cart.id, cart.amount, True)
        text = f'Your order {cart.id} was approved successfully!'
        await bot.bot.send_message(cart.id_user, text=text)

    await message.answer('All orders were approved. /orders_', reply_markup=ReplyKeyboardRemove())


class Approval(StatesGroup):
    action = State()
    cart_id = State()


@admin_router.message((F.text == "Approve") | (F.text == "Reject"))
async def approve_reject_process(message: Message, session: AsyncSession, state: FSMContext):
    await state.set_state(Approval.action)
    await state.update_data(action=message.text)

    await state.set_state(Approval.cart_id)
    await message.answer('Please, enter a number #', parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())


@admin_router.message(Approval.cart_id)
async def approve_reject_process_end(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(cart_id=message.text)

    data = await state.get_data()

    cart_id = int(data['cart_id'])
    action = data['action']

    cart = await get_cart(session, cart_id)
    product = await get_product(session, cart.id_product)

    if action == 'Approve':
        await update_cart(session, cart_id, cart.amount, True)
        text = f'Your order {cart.id} was approved successfully!'
        await bot.bot.send_message(cart.id_user, text=text)
        await message.answer(f'Order {cart.id} was approved.')

    elif action == 'Reject':
        text = (f'Unfortunately, your order {cart_id} was rejected.\n' +
                hstrikethrough(f'{product.title}, {product.amount}'))

        await bot.bot.send_message(cart.id_user, text=text)
        await message.answer(f'Order {cart.id} was rejected.')
        await delete_cart(session, cart_id)

    await state.clear()


#   See orders
@admin_router.message(Command('_products'))
async def products_cmd(message: Message, session: AsyncSession):
    table = PrettyTable()

    table.title = "Products"

    table.field_names = ['#', 'Title', 'Price', 'Amount']

    products = await list_products(session=session)
    for product in products:
        table.add_row([f'{product.id}',
                       f'{product.title}',
                       f'{product.price}',
                       f'{product.amount}'])

    text = f'`{table.get_string()}`'

    await message.answer(text, parse_mode='Markdown')


#   See, Edit, Add, Delete products
class ProductsAdd(StatesGroup):
    title = State()
    price = State()
    amount = State()


@admin_router.message(Command('_product_add'))
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

# TODO: delete products
# TODO: edit amount of product
# TODO: apply keyboard to admin
# TODO: indexing
# TODO: statistics (amount of users, orders)
# TODO: list approved orders
