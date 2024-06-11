import pytest
from decimal import Decimal

import fastapi
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import restaurant_menu.utils.log_config as log_config
from restaurant_menu.core.config import settings
from restaurant_menu.models.database import (
    Base, Client, Dish, Feedback, Order, Restaurant)

sync_engine = create_engine(
    url=settings.TEST_DATABASE_URL,
    echo=True,
)
session_factory = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
)


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.
    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="module")
def fastapi_app() -> fastapi.FastAPI:
    """
    Fixture to create FastAPI.
    :return: Fastapi app with mocked dependencies.
    """
    from restaurant_menu.app import app

    return app


@pytest.fixture(scope="module")
async def async_client(
     fastapi_app: fastapi.FastAPI,
     anyio_backend: str) -> httpx.AsyncClient:
    async with httpx.AsyncClient(
         app=fastapi_app,
         base_url="http://test") as client:
        log_config.log.info("Клиент готов...")
        yield client


@pytest.fixture(scope="class")
def prepare_db_creating():
    Base.metadata.create_all(sync_engine)
    yield
    Base.metadata.drop_all(sync_engine)


@pytest.fixture(scope="function")
def prepare_db_relation():
    Base.metadata.create_all(sync_engine)
    yield
    Base.metadata.drop_all(sync_engine)


@pytest.fixture
def restaurants():
    restaraunts = [
        Restaurant(name="Istanbul Han Halal"),
        Restaurant(name="KFC"),
    ]
    return restaraunts


@pytest.fixture
def clients():
    clients = [
        Client(chat_id=8656453, name="Valentin"),
        Client(chat_id=6543456, name="Oleg"),
        Client(chat_id=8765346, name="Vadim"),
        Client(chat_id=2345776, name="Sergay"),
        Client(chat_id=1467964, name="Feofil"),
    ]
    return clients


@pytest.fixture
def feedbacks():
    feedbacks = [
        Feedback(
            author_id=1,
            feedback="Супер рестик",
            stars=5,
            restaurant_id=1,),
        Feedback(
            author_id=1,
            feedback="збс",
            stars=5,
            restaurant_id=2,),
        Feedback(
            author_id=2,
            feedback="Хуйня, а не рестик",
            stars=1,
            restaurant_id=1,),
        Feedback(
            author_id=3,
            feedback="Норм рестик",
            stars=3,
            restaurant_id=2,),
    ]
    return feedbacks


@pytest.fixture
def dishes():
    dishes = [
        Dish(
            name="Шавуха",
            cost=Decimal(149.99),
            type="Основное",
            description="Песдатая шавуха",
            restaurant_id=1
        ),
        Dish(
            name="Чай",
            cost=Decimal(49.99),
            type="Напиток",
            description="Песдатый чай",
            restaurant_id=1
        ),
        Dish(
            name="Борщ",
            cost=Decimal(99.50),
            type="Суп",
            description="Охуенный Истамбуловский борщец",
            restaurant_id=1
        ),
        Dish(
            name="Пахлава",
            cost=Decimal(25.49),
            type="Десерт",
            description="Жопа слипнется",
            restaurant_id=1
        ),
        Dish(
            name="Цезарь",
            cost=Decimal(50),
            type="Салат",
            description="Со вкусом ножа в спину",
            restaurant_id=1
        ),
        Dish(
            name="Плов",
            cost=Decimal(201.99),
            type="Основное",
            description="Охапка дров и плов готов",
            restaurant_id=1
        ),
        Dish(
            name="Кофе",
            cost=Decimal(9.99),
            type="Напиток",
            description="Крепкий как жопа той телки",
            restaurant_id=1
        ),
        Dish(
            name="Уха",
            cost=Decimal(20.99),
            type="Суп",
            description="Супец из ухуенной рыбки",
            restaurant_id=1
        ),
        Dish(
            name="Мороженое",
            cost=Decimal(27.99),
            type="Десерт",
            description="Мясо",
            restaurant_id=1
        ),
        Dish(
            name="Греческий",
            cost=Decimal(15.99),
            type="Салат",
            description="Со вкусом гнета Османской Империи",
            restaurant_id=1
        ),
    ]
    return dishes


@pytest.fixture
def orders():
    orders = [
        Order(
            comment="Вне очереди",
            client_id=1,
        )
    ]
    return orders
