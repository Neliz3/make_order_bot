from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, BotCommandScopeAllPrivateChats
from aiogram.filters import Command
from aiogram import Router, F, Bot
from aiogram.filters.callback_data import CallbackQuery

from prettytable import PrettyTable

from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import commands
from app.keyboards.keyboard import (keyboard_choose_product as kb, keyboard_edit_del,
                                    keyboard_choose_amount as amount_key,
                                    QueryCallback)
from app.db.queries import (add_user, list_products, get_carts_by_user, get_product,
                            delete_cart, update_cart, get_cart, update_user)

from app.handlers.callbacks import callback_router
from app.filters import chat

user_router = Router()
user_router.message.filter(chat.ChatFilter())

"""     Registration, Send the instruction      """


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    address = State()
    phone = State()


@user_router.message(Command('start'))
async def start_command(message: Message, state: FSMContext, bot: Bot):
    await bot.set_my_commands(commands.commands, scope=BotCommandScopeAllPrivateChats())

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

    try:
        await update_user(session,
                          id_=message.from_user.id,
                          first_name=first_name,
                          last_name=last_name,
                          address=address,
                          phone=phone)
    except ():
        await add_user(session,
                       tg_id=message.from_user.id,
                       first_name=first_name,
                       last_name=last_name,
                       address=address,
                       phone=phone)

    answer = f'Name: {first_name} {last_name}\nPhone: {phone}\nAddress: {address} was added.'
    await message.answer(text=answer)
    await message.answer('If you want to edit information, click /start again.')

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


"""     Change amount, Delete a Cart      """


@user_router.message(Command('cart'))
async def cart_command(message: Message, session: AsyncSession):
    id_user = message.from_user.id

    result = await get_carts_by_user(session, id_user)
    total_price = 0

    table = PrettyTable()

    table.title = "Your Cart"

    table.field_names = ['#', 'Title', 'Price', 'Amount']

    for cart in result:
        product = await get_product(session, cart.id_product)

        product_total_price = int(cart.amount) * int(product.price)

        table.add_row([f'{cart.id}',
                       f'{product.title}',
                       f'{product_total_price}',
                       f'{cart.amount}'])

        total_price += product_total_price

    text = f'`{table.get_string()}\nTotal price   {total_price}`'

    await message.answer(text, parse_mode='Markdown', reply_markup=await keyboard_edit_del())


class Delete(StatesGroup):
    product_id = State()


@user_router.message(F.text == "Delete")
async def delete_process(message: Message, session: AsyncSession, state: FSMContext):
    await state.set_state(Delete.product_id)
    await message.answer('Please, enter a number #', parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())


@user_router.message(Delete.product_id)
async def delete_process_end(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(product_id=message.text)
    data = await state.get_data()
    try:
        await delete_cart(session, int(data['product_id']))
        await state.clear()
        await message.answer('Product deleted from a /cart')
    except ():
        await message.answer('Something went wrong... Try again /cart')


class Edit(StatesGroup):
    cart_id = State()
    amount = State()


@user_router.message(F.text == "Edit")
async def edit_process(message: Message, session: AsyncSession, state: FSMContext):
    await state.set_state(Edit.cart_id)
    await message.answer('Please, enter a number #', reply_markup=ReplyKeyboardRemove())


@user_router.message(Edit.cart_id)
async def edit_process_two(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(cart_id=message.text)

    data = await state.get_data()

    cart = await get_cart(session, int(data['cart_id']))
    await message.answer('Please, choose an amount',
                         reply_markup=await amount_key(session, id_product=cart.id_product,
                                                       action='edit_cart'))


@user_router.callback_query(QueryCallback.filter(F.action == "edit_cart"))
@user_router.message(Edit.amount)
async def edit_process_end(query: CallbackQuery, callback_data: QueryCallback, session: AsyncSession,
                           state: FSMContext):
    id_user = query.from_user.id

    data = await state.get_data()

    cart_id = int(data['cart_id'])
    amount = int(callback_data.value)

    await state.update_data(amount=amount)

    await update_cart(session=session,
                      id_=cart_id,
                      amount=amount,
                      approval=False)

    table = PrettyTable()

    table.field_names = ['#', 'Title', 'Price', 'Amount', 'Total']

    cart = await get_cart(session, cart_id)
    product = await get_product(session, cart.id_product)

    table.add_row([f'{cart_id}',
                   f'{product.title}',
                   f'{product.price}',
                   f'{amount}',
                   f'{product.price * amount}'])

    text = f'`{table.get_string()}`'

    await query.message.edit_text(text, parse_mode='Markdown')
    await query.message.answer('Product successfully edited. /cart', reply_markup=ReplyKeyboardRemove())


"""     Send instructions        """


@user_router.message(Command('help'))
async def help_command(message: Message):
    await message.answer("Help")


"""     Unrecognized messages       """


@callback_router.message(Command("cancel"))
@user_router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Cancelled.", reply_markup=ReplyKeyboardRemove())


@user_router.message()
async def undefined_handler(message: Message):
    await message.answer(f"Dear, {message.from_user.full_name}, I do not understand you. Try again, please )")
