from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app import keyboards as key
from app.db.queries import add_user

user_router = Router()


"""     Register, Send the instruction      """


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    address = State()
    phone = State()


@user_router.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext):
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


#   TODO: Middleware does not see session

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


"""     Change amount, Delete, Approve      """


@user_router.message(Command('view_cart'))
async def command_start_handler(message: Message):
    await message.answer("cart")


"""     See products, Add to cart, Choose amount      """


@user_router.message(Command('products'))
async def command_start_handler(message: Message):
    await message.answer("products",  reply_markup=key.inline.builder.as_markup())


"""     Send instruction        """


@user_router.message(Command('help'))
async def command_start_handler(message: Message):
    await message.answer("Help")


"""     Unrecognized messages       """


@user_router.message()
async def command_echo_handler(message: Message):
    await message.answer(f"Dear, {message.from_user.full_name}, I do not understand you. Try again, please )")


