import os
import typing as tp
from urllib.parse import quote_plus

import pydantic as pd


class Settings(pd.BaseSettings):
    """
    Settings
    """

    DEBUG: bool = False
    BACKEND_CORS_ORIGINS: tp.List[tp.Union[pd.AnyHttpUrl, str]] = ["http://localhost"]  # type: ignore

    ID_MIN: int = 1

    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: str
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DATABASE: str
    POSTGRESQL_SCHEMA: str
    DATABASE_URI: tp.Optional[pd.PostgresDsn] = None
    TEST_DATABASE_URL: str

    NODOC: bool = False
    API_ROOT_URL: str = ""
    LOG_WRITER: str = "stdout"  # stdout | tcp://0.0.0.0:5170
    LOG_FORMAT: str = "dev"  # plaintext | json | dev
    LOG_BACKTRACE: bool = False
    LOG_DIAGNOSE: bool = False

    @pd.validator("DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls,
        value: tp.Optional[str],
        values: tp.Dict[str, tp.Any],  # noqa: N805, WPS110
    ) -> str:
        if isinstance(value, str):
            return value

        return pd.PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRESQL_USER"),
            password=quote_plus(values.get("POSTGRESQL_PASSWORD")),
            host=values.get("POSTGRESQL_HOST"),
            port=values.get("POSTGRESQL_PORT"),
            path="/{0}".format(values.get("POSTGRESQL_DATABASE")),
            # query=f"schema={values.get("POSTGRESQL_SCHEMA")}",
        )

    @pd.validator("BACKEND_CORS_ORIGINS", pre=True)
    def set_backend_cors_origins(
        cls,
        v: tp.List[str],
        values: tp.Dict[str, tp.Any],  # noqa: N805, WPS110
    ) -> tp.List[str]:
        if values.get("DEBUG", False):
            return ["*"]
        return v

    class Config(object):
        env_prefix = ""  # prefix for env variables, defaults to no prefix, i.e. ""
        case_sensitive = True


# Load secrets from a file on SECRETS_PATH_DB in dotenv format.
settings = Settings(_env_file=os.environ.get("SECRETS_PATH_DB"))
