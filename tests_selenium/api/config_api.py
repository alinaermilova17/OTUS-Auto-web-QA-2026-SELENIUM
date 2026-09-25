import os
from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL", "https://restful-booker.herokuapp.com")

if not BASE_API_URL:
    raise ValueError("BASE_API_URL не задан")