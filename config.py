import os
from dotenv import load_dotenv

load_dotenv()


LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
BASE_URL = os.getenv('BASE_URL', 'http://prestashop:80')
BASE_API_URL = os.getenv("BASE_API_URL", "https://restful-booker.herokuapp.com")

if not all([LOGIN, PASSWORD, BASE_URL]):
    raise ValueError('Не все переменные окружения загружены! Проверьте .env файл.')