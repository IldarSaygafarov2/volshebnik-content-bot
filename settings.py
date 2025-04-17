import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_LINK = os.getenv("SPREADSHEET_LINK")
API_URL = os.getenv("API_URL")
