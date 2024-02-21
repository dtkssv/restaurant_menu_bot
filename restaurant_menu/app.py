import uvicorn
from fastapi import FastAPI
from .models.database import lifespan
from .middlewares import request_handler
from .routers import setup_routes
from .routers import TAGS_METADATA
from .settings import api_settings, api_docs_settings

app = FastAPI(
    title=api_docs_settings.title,
    version=api_docs_settings.version,
    openapi_tags=TAGS_METADATA,
    lifespan=lifespan
)
app.middleware("http")(request_handler)
setup_routes(app)


def run():
    """Run the API using Uvicorn"""
    uvicorn.run(app, host=api_settings.host, port=api_settings.port)


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}