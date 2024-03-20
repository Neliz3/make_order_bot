from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Users, Products, Carts

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
async def update_user(session: AsyncSession, id_, first_name, last_name, address, phone):
    query = (update(Users).where(Users.tg_id == id_).
             values(first_name=first_name).values(last_name=last_name).
             values(address=address).values(phone=phone))
    await session.execute(query)
    await session.commit()


#   Delete User
async def delete_user(session: AsyncSession, id_):
    query = delete(Users).where(Users.id == id_)
    await session.execute(query)
    await session.commit()


""" CRUD For Products """


#   Add Product
async def add_product(session: AsyncSession, title, price, amount):
    session.add(Products(title=title, price=price, amount=amount))
    await session.commit()


#   List Products
async def list_products(session: AsyncSession):
    query = select(Products)
    result = await session.execute(query)
    return result.scalars().all()


#   Get particular Product
async def get_product(session: AsyncSession, id_):
    query = select(Products).where(Products.id == id_)
    result = await session.execute(query)
    return result.scalar()


#   Update Product
async def update_product(session: AsyncSession, id_, title, price, amount):
    query = (
        update(Products).where(Products.id == id_).
        values(title=title).values(price=price).values(amount=amount))
    await session.execute(query)
    await session.commit()


#   Delete Product
async def delete_product(session: AsyncSession, id_):
    query = delete(Products).where(Products.id == id_)
    await session.execute(query)
    await session.commit()


""" CRUD For Carts """


#   Add Cart
async def add_cart(session: AsyncSession, id_user, id_product, amount, approval):
    session.add(Carts(id_user=id_user,
                      id_product=id_product,
                      amount=amount,
                      approval=approval))
    await session.commit()


#   List Carts
async def list_carts(session: AsyncSession):
    query = select(Carts)
    result = await session.execute(query)
    return result.scalars().all()


#   Get particular Carts
async def get_carts_by_user(session: AsyncSession, id_user):
    query = select(Carts).where(Carts.id_user == id_user)
    result = await session.execute(query)
    return result.scalars().all()


#   Get approved Carts
async def get_carts_approved(session: AsyncSession):
    query = select(Carts).where(Carts.approval == True)
    result = await session.execute(query)
    return result.scalars().all()


#   Get particular Cart by product and user
async def get_cart_by_product(session: AsyncSession, id_user, id_product):
    query = select(Carts).where(Carts.id_user == id_user).where(Carts.id_product == id_product)
    result = await session.execute(query)
    return result.scalar()


#   Get particular Cart
async def get_cart(session: AsyncSession, id_cart):
    query = select(Carts).where(Carts.id == id_cart)
    result = await session.execute(query)
    return result.scalar()


#   Update Cart
async def update_cart(session: AsyncSession, id_, amount, approval):
    query = (
        update(Carts).where(Carts.id == id_).values(amount=amount).values(approval=approval))
    await session.execute(query)
    await session.commit()


#   Delete Cart
async def delete_cart(session: AsyncSession, id_):
    query = delete(Carts).where(Carts.id == id_)
    await session.execute(query)
    await session.commit()
