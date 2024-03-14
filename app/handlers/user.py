from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import Router, F

from prettytable import PrettyTable

from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.keyboard import keyboard_products as kb
from app.db.queries import add_user, list_products, get_cart, get_product

from app.handlers.callbacks import callback_router
from app.handlers.admin import admin_router

user_router = Router()


"""     Registration, Send the instruction      """


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    address = State()
    phone = State()


@user_router.message(Command('start'))
async def start_command(message: Message, state: FSMContext):
    await state.set_state(Registration.first_name)
    await message.answer(f"Hi! What's your first name?")


@user_router.message(Registration.first_name)
async def process_first_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    await state.set_state(Registration.last_name)
    await message.answer(f"What's your last name?")


@user_router.message(Registration.last_name)
async def process_last_name(message: Message, state: FSMContext) -> None:
    await state.update_data(last_name=message.text)
    await state.set_state(Registration.address)
    await message.answer(f"Give me your address, please")


@user_router.message(Registration.address)
async def process_address(message: Message, state: FSMContext) -> None:
    await state.update_data(address=message.text)
    await state.set_state(Registration.phone)
    await message.answer(f"Give me your number, please")


@user_router.message(Registration.phone)
async def process_phone(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(phone=message.text)

    data = await state.get_data()
    await state.clear()

    await add_to_database(message, data, session=session)


async def add_to_database(message: Message, data: Dict[str, Any], session):
    first_name = data["first_name"]
    last_name = data["last_name"]
    address = data["address"]
    phone = data["phone"]

    await add_user(session,
                   tg_id=message.from_user.id,
                   first_name=first_name,
                   last_name=last_name,
                   address=address,
                   phone=phone)

    answer = first_name + last_name + phone + address + "was added"
    await message.answer(text=answer)


"""     See products, Add to cart, Choose amount      """


@user_router.message(Command('products'))
async def products_command(message: Message, session: AsyncSession):
    result = await list_products(session)

    table = PrettyTable()

    table.field_names = ['#', 'Title', 'Price']

    table.title = "Products"

    for product in result:
        table.add_row([f'{product.id}', f'{product.title}', f'{product.price}'])

    text = f'`{table.get_string()}`'
    await message.answer(text,
                         reply_markup=await kb(session),
                         parse_mode='Markdown')


"""     Change amount, Delete, Approve a Cart      """


@user_router.message(Command('cart'))
async def cart_command(message: Message, session: AsyncSession):
    ### TODO: indexing of a database

    id_user = message.from_user.id

    result = await get_cart(session, id_user)
    total_price = 0

    table = PrettyTable()

    table.title = "Your Cart"

    table.field_names = ['#', 'Title', 'Price', 'Amount']

    for cart in result:
        product = await get_product(session, cart.id_product)

        product_total_price = int(cart.amount) * int(product.price)

        table.add_row([f'{product.id}',
                       f'{product.title}',
                       f'{product_total_price}',
                       f'{cart.amount}'])

        total_price += product_total_price

    text = f'`{table.get_string()}\nTotal price   {total_price}`'

    await message.answer(text, parse_mode='Markdown')


"""     Send instructions        """


@user_router.message(Command('help'))
async def help_command(message: Message):
    await message.answer("Help")


"""     Unrecognized messages       """


@user_router.message(Command("cancel"))
@user_router.message(F.text.casefold() == "cancel")
@callback_router.message(Command("cancel"))
@callback_router.message(F.text.casefold() == "cancel")
@admin_router.message(Command("cancel"))
@admin_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Cancelled.", reply_markup=ReplyKeyboardRemove())


@user_router.message()
async def undefined_handler(message: Message):
    await message.answer(f"Dear, {message.from_user.full_name}, I do not understand you. Try again, please )")


