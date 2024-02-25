from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from dotenv import load_dotenv
import os


load_dotenv()


#   Connecting db
DB = os.getenv("DB")
USER = os.getenv("USER")
HOST = os.getenv("HOST")
PASSWD = os.getenv("PASSWD")
DB_NAME = os.getenv("DB_NAME")
PORT = os.getenv("PORT")

url = f'{DB}://{USER}:{PASSWD}@{HOST}:{PORT}/{DB_NAME}'

Base = declarative_base()
engine = create_async_engine(url, echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
