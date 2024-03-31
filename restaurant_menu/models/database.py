from datetime import datetime
from sqlalchemy import (create_engine, MetaData, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger,
                        SmallInteger, Table)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from fastapi import FastAPI
from contextlib import asynccontextmanager

SQLALCHEMY_DATABASE_URL = "postgresql://bot:12345@localhost:5432/res_meny"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()
Base.metadata = metadata


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), unique=True)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    author = Column(ForeignKey("client.id"))
    feedback = Column(String(500))
    stars = Column(Integer)
    restaurant_id = Column(ForeignKey("restaurant.id"))
    client_id = Column(ForeignKey("client.id"))


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True)
    name = Column(String)


DisheOrder = Table('DisheOrder', Base.metadata,
    Column('dishe_id', Integer(), ForeignKey("dishe.id")),
    Column('order_id', Integer(), ForeignKey("order.id"))
)


class Dishe(Base):
    __tablename__ = "dishe"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cost = Column(Float)
    type = Column(String(20))
    description = Column(String(500))
    restaurant_id = Column(ForeignKey("restaurant.id"))


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    dish = Column(String(50))
    cost = Column(Float)
    data = Column(DateTime, default=datetime.now)
    comment = Column(String(500))
    client_id = Column(ForeignKey("client.id"))
    dish_replied = relationship("Dishe", secondary=DisheOrder)


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
