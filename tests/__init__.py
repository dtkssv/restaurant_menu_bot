import os
from pathlib import Path

from dotenv import load_dotenv

# Инициализация переменных виртуального окружения
path_input = Path(__file__).parent.parent / ".env"
if path_input.exists():
    load_dotenv(path_input)
    os.environ["SECRETS_PATH_DB"] = str(path_input)
