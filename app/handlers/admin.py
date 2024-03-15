from aiogram.types import Message, ReplyKeyboardRemove, BotCommandScopeAllPrivateChats
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F, Bot
from aiogram.utils.markdown import hstrikethrough

from sqlalchemy.ext.asyncio import AsyncSession

from prettytable import PrettyTable

from typing import Dict, Any

from app.filters import admin, chat
from app.keyboards.keyboard import keyboard_approve, keyboard_edit_del_product
from app.keyboards import commands

from app.db.queries import (list_users,
                            add_product, list_carts, list_products, get_product, get_cart,
                            update_cart, delete_cart, delete_product, update_product)

admin_router = Router()
admin_router.message.filter((admin.IsAdmin()) and (chat.ChatFilter()))


@admin_router.message(Command('admin_set'))
async def admin_cmd(message: Message, bot: Bot):
    await bot.set_my_commands(commands.admin_commands, scope=BotCommandScopeAllPrivateChats())

    await message.answer(f"Admin mode was set up.")


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
async def approve_all_process(message: Message, session: AsyncSession, bot: Bot):
    carts = await list_carts(session=session)
    for cart in carts:
        await update_cart(session, cart.id, cart.amount, True)
        text = f'Your order {cart.id} was approved successfully!'
        await bot.send_message(cart.id_user, text=text)

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
async def approve_reject_process_end(message: Message, session: AsyncSession, state: FSMContext,
                                     bot: Bot):
    await state.update_data(cart_id=message.text)

    data = await state.get_data()

    cart_id = int(data['cart_id'])
    action = data['action']

    cart = await get_cart(session, cart_id)
    product = await get_product(session, cart.id_product)

    if action == 'Approve':
        await update_cart(session, cart_id, cart.amount, True)
        text = f'Your order {cart.id} was approved successfully!'
        await bot.send_message(cart.id_user, text=text)
        await message.answer(f'Order {cart.id} was approved.')

    elif action == 'Reject':
        text = (f'Unfortunately, your order {cart_id} was rejected.\n' +
                hstrikethrough(f'{product.title}, {product.amount}'))

        await bot.send_message(cart.id_user, text=text)
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

    await message.answer(text, parse_mode='Markdown', reply_markup=await keyboard_edit_del_product())


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
async def product_process_price(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(ProductsAdd.price)
    await message.answer("Enter a product price")


@admin_router.message(ProductsAdd.price)
async def product_process_amount(message: Message, state: FSMContext) -> None:
    await state.update_data(price=message.text)
    await state.set_state(ProductsAdd.amount)
    await message.answer("Enter a product amount")


@admin_router.message(ProductsAdd.amount)
async def product_process_end(message: Message, state: FSMContext, session: AsyncSession):
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


# TODO: indexing
# TODO: statistics (amount of users, orders)
# TODO: list approved orders


class Delete(StatesGroup):
    product_id = State()


@admin_router.message(F.text == "Delete Product")
async def delete_process(message: Message, session: AsyncSession, state: FSMContext):
    await state.set_state(Delete.product_id)
    await message.answer('Please, enter a number #', parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())


@admin_router.message(Delete.product_id)
async def delete_product_end(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(product_id=message.text)
    data = await state.get_data()
    try:
        await delete_product(session, int(data['product_id']))
        await state.clear()
        await message.answer('Product was deleted.')
    except ():
        await message.answer('Error occurred. Try again.')


class Edit(StatesGroup):
    product_id = State()
    title = State()
    amount = State()
    price = State()


@admin_router.message(F.text == "Edit Product")
async def edit_process(message: Message, session: AsyncSession, state: FSMContext):
    await state.set_state(Edit.product_id)
    await message.answer('Please, enter a number #', reply_markup=ReplyKeyboardRemove())


@admin_router.message(Edit.product_id)
async def edit_process_id(message: Message, state: FSMContext):
    await state.update_data(product_id=message.text)
    await state.set_state(Edit.title)
    await message.answer('Please, enter a title.')


@admin_router.message(Edit.title)
async def edit_process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Edit.amount)
    await message.answer('Please, enter an amount.')


@admin_router.message(Edit.amount)
async def edit_process_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(Edit.price)
    await message.answer('Please, enter a price.')


@admin_router.message(Edit.price)
async def edit_process_price(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(price=message.text)
    data = await state.get_data()
    product_id = int(data['product_id'])
    title = data['title']
    amount = int(data['amount'])
    price = int(data['price'])

    await update_product(session, product_id, title, price, amount)
    await message.answer(f'Product {product_id} was edited. /_products')
