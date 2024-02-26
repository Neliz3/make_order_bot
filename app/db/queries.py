from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Users

""" CRUD For Users """


#   Add User
async def add_user(session: AsyncSession, tg_id, first_name, last_name, address, phone):
    session.add(Users(tg_id=tg_id, first_name=first_name, last_name=last_name, address=address, phone=phone))
    await session.commit()


#   List Users
async def list_users(session: AsyncSession):
    query = select(Users)
    result = await session.execute(query)
    return result.scalars().all()


#   Get particular User
async def get_user(session: AsyncSession, id_):
    query = select(Users).where(Users.id == id_)
    result = await session.execute(query)
    return result.scalar()


#   Update User
async def update_user(session: AsyncSession, id_, address, phone):
    query = update(Users).where(Users.id == id_).values(address=address).values(phone=phone)
    await session.execute(query)
    await session.commit()


#   Delete User
async def delete_user(session: AsyncSession, id_):
    query = delete(Users).where(Users.id == id_)
    await session.execute(query)
    await session.commit()
