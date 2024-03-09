from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from contextlib import asynccontextmanager

SQLALCHEMY_DATABASE_URL = "postgresql://bot:12345@localhost:5432/res_meny"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова")


async def create_tables():
    async with engine.begin() as conn:
        await conn.runn_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.runn_sync(Base.metadata.create_all)
