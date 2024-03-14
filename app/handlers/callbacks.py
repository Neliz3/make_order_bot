from aiogram import Router, F

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from prettytable import PrettyTable

from app.keyboards.keyboard import (QueryCallback,
                                    keyboard_to_cart,
                                    keyboard_choose_amount)

from app.db.queries import add_cart, get_product, get_cart, update_cart, get_cart_by_product

callback_router = Router()


class Cart(StatesGroup):
    product_id = State()
    amount = State()


@callback_router.callback_query(QueryCallback.filter(F.action == "add"))
async def cart(query: CallbackQuery, callback_data: QueryCallback, session: AsyncSession, state: FSMContext):
    id_product = callback_data.value

    await state.update_data(product_id=id_product)
    await state.set_state(Cart.amount)
    await state.update_data(amount='1')

    table = PrettyTable()

    table.field_names = ['#', 'Title', 'Price', 'Amount']

    product = await get_product(session, id_product)

    table.add_row([f'{product.id}',
                   f'{product.title}',
                   f'{product.price}',
                   '1'])

    text = f'`{table.get_string()}`'

    await query.message.edit_text(text, parse_mode='Markdown')
    await query.message.answer(text='Enter /products to choose another product',
                               reply_markup=await keyboard_to_cart(),
                               parse_mode='Markdown')


@callback_router.message(F.text == "Amount")
async def ask_amount(message: Message, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    product_id = data['product_id']

    await message.answer('Enter an amount',
                         reply_markup=await keyboard_choose_amount(session, id_product=product_id, action='amount'))


@callback_router.callback_query(QueryCallback.filter(F.action == "amount"))
async def process_amount(query: CallbackQuery, callback_data: QueryCallback, session: AsyncSession, state: FSMContext):
    id_user = query.from_user.id

    data = await state.get_data()

    product_id = data['product_id']
    amount = int(callback_data.value)

    await state.update_data(amount=amount)

    await add_cart(session=session,
                       id_user=id_user,
                       id_product=product_id,
                       amount=amount,
                       approval=False)

    table = PrettyTable()

    table.field_names = ['#', 'Title', 'Price', 'Amount', 'Total']

    product = await get_product(session, product_id)

    table.add_row([f'{product.id}',
                   f'{product.title}',
                   f'{product.price}',
                   f'{amount}',
                   f'{product.price * amount}'])

    text = f'`{table.get_string()}`'

    await query.message.edit_text(text, parse_mode='Markdown')
    await query.message.answer('Product successfully added to /cart.', reply_markup=ReplyKeyboardRemove())


@callback_router.message(F.text == "Add to Cart")
async def add_to_cart(message: Message, session: AsyncSession, state: FSMContext):
    id_user = message.from_user.id

    data = await state.get_data()

    product_id = data['product_id']
    amount = int(data['amount'])

    await add_cart(session=session,
                   id_user=id_user,
                   id_product=product_id,
                   amount=amount,
                   approval=False)

    table = PrettyTable()

    table.field_names = ['#', 'Title', 'Price', 'Amount', 'Total']

    product = await get_product(session, product_id)

    table.add_row([f'{product.id}',
                   f'{product.title}',
                   f'{product.price}',
                   f'{amount}',
                   f'{product.price * amount}'])

    text = f'`{table.get_string()}`'

    await message.answer(text, parse_mode='Markdown')
    await state.clear()
    await message.answer('Product successfully added to /cart.', reply_markup=ReplyKeyboardRemove())
