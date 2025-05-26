import os
from dotenv import load_dotenv

load_dotenv(".env")


BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_LINK = os.getenv("SPREADSHEET_LINK")
API_URL = os.getenv("API_URL", None)
print(API_URL)

HEADERS = [
    "№",
    "Баркод",
    "Название",
    "Издательство",
    "Описание",
    "Возраст",
    "Габариты см",
    "Кол-во страниц",
    "Переплёт",
    "Категория",
    "Под категория",
    "Цена",
    "Ссылка на фото",
]
