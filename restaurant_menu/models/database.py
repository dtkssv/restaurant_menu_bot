from datetime import datetime
from sqlalchemy import (create_engine, MetaData, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger,
                        SmallInteger, Table)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from fastapi import FastAPI
from contextlib import asynccontextmanager

SQLALCHEMY_DATABASE_URL = "postgresql://bot:12345@localhost:5432/res_meny"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
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


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True)
    name = Column(String)


# Dish_Order = Table('Dish_Order',
#                    Base.metadata,
#                    Column('dish_id', ForeignKey("dish.id"), primary_key=True),
#                    Column('order_id', ForeignKey("order.id"), primary_key=True)
# )

class Dish_Order(Base):
    __tablename__ = "Dish_Order"
    dish_id = Column(ForeignKey("dish.id"), primary_key=True)
    order_id = Column(ForeignKey("order.id"), primary_key=True)
    dish = relationship("Dish", back_populates="orders")
    order = relationship("Order", back_populates="dishes")

class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cost = Column(Float)
    type = Column(String(20))
    description = Column(String(500))
    restaurant_id = Column(ForeignKey("restaurant.id"))
    orders = relationship("Dish_Order", back_populates="dish")
    # order = relationship("Order", secondary=Dish_Order, back_populates='dish')


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, default=datetime.now)
    comment = Column(String(500), nullable=True)
    client_id = Column(ForeignKey("client.id"))
    dishes = relationship("Dish_Order", back_populates="order")
    # dish = relationship("Dish", secondary=Dish_Order, back_populates='order')


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
