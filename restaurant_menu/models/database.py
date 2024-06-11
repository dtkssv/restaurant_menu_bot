from datetime import datetime
from typing import Annotated, Optional, List

# from fastapi import FastAPI
# from contextlib import asynccontextmanager
from sqlalchemy import (BigInteger, DECIMAL, ForeignKey, String, create_engine)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            relationship, sessionmaker)

from restaurant_menu.core.config import settings

sync_engine = create_engine(
    url=str(settings.DATABASE_URI),
    echo=True,
)
session_factory = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
)

# async_engine = create_async_engine(
#     url=str(settings.DATABASE_URI),
#     echo=True,
# )
# async_session_factory = async_sessionmaker(
#     bind=async_engine,
#     expire_on_commit=False,
# )

str_20 = Annotated[str, 20]
str_50 = Annotated[str, 50]
str_200 = Annotated[str, 50]
str_500 = Annotated[str, 500]
intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_20: String(20),
        str_50: String(50),
        str_200: String(200),
        str_500: String(500),
    }


class Restaurant(Base):
    __tablename__ = "restaurant"
    id: Mapped[intpk]
    name: Mapped[str_50] = mapped_column(unique=True)
    feedbacks: Mapped[List["Feedback"]] = relationship(
        back_populates="restaurant",
    )
    restaurant_dishes: Mapped[List["Dish"]] = relationship(
        back_populates="restaurant",
    )


class Client(Base):
    __tablename__ = "client"
    id: Mapped[intpk]
    chat_id = mapped_column(BigInteger, unique=True)
    name: Mapped[str_200]
    orders: Mapped[List["Order"]] = relationship(
        back_populates=""
    )
    feedbacks: Mapped[List["Feedback"]] = relationship(
        back_populates="feedback_author",
    )


class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[intpk]
    author_id: Mapped[int] = mapped_column(ForeignKey(
        "client.id",  ondelete="CASCADE"))
    feedback: Mapped[str_500]
    stars: Mapped[str_20]
    restaurant_id: Mapped[int] = mapped_column(ForeignKey(
        "restaurant.id", ondelete="CASCADE"))
    feedback_author: Mapped["Client"] = relationship(
        back_populates="feedbacks",
    )
    restaurant: Mapped["Restaurant"] = relationship(
        back_populates="feedbacks",
    )


class Order(Base):
    __tablename__ = "order"

    id: Mapped[intpk]
    date: Mapped[datetime] = mapped_column(default=datetime.now)
    comment: Mapped[Optional[str_500]]
    client_id: Mapped[int] = mapped_column(ForeignKey(
        "client.id", ondelete="CASCADE"))
    client: Mapped["Client"] = relationship(
        back_populates="orders",
    )
    dishes: Mapped[List["Dish"]] = relationship(
        secondary="dish_order",
        back_populates="orders",
    )


class Dish(Base):
    __tablename__ = "dish"
    id: Mapped[intpk]
    name: Mapped[str_50]
    cost = mapped_column(DECIMAL(10, 4), default=0)
    type: Mapped[str_20]
    description: Mapped[str_500]
    restaurant_id: Mapped[int] = mapped_column(ForeignKey(
        "restaurant.id", ondelete="CASCADE"))
    restaurant: Mapped["Restaurant"] = relationship(
        back_populates="restaurant_dishes",
    )
    orders: Mapped[List["Order"]] = relationship(
        secondary="dish_order",
        back_populates="dishes",
    )


class DishOrder(Base):
    __tablename__ = "dish_order"
    dish_id: Mapped[int] = mapped_column(
        ForeignKey("dish.id", ondelete="CASCADE"),
        primary_key=True,
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.id", ondelete="CASCADE"),
        primary_key=True,
    )


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await delete_tables()
#     print("База очищена")
#     await create_tables()
#     print("База готова")


# async def create_tables():
#     async with sync_engine.begin() as conn:
#         await conn.runn_sync(Base.metadata.create_all)


# async def delete_tables():
#     async with sync_engine.begin() as conn:
#         await conn.runn_sync(Base.metadata.create_all)
