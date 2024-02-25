from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

from conf import url

Base = declarative_base()
engine = create_async_engine(url, echo=True, poolclass=AsyncAdaptedQueuePool, pool_size=200, max_overflow=10)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
