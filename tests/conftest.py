import pytest

import fastapi
import httpx

import restaurant_menu.utils.log_config as log_config


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
async def async_client(fastapi_app: fastapi.FastAPI, anyio_backend: str) -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=fastapi_app, base_url="http://test") as client:
        log_config.log.info("Клиент готов...")
        yield client
