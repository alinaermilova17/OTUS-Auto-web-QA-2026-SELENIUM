import os
from dotenv import load_dotenv

load_dotenv()


LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
BASE_URL = os.getenv('BASE_URL', 'http://prestashop:80')

if not all([LOGIN, PASSWORD, BASE_URL]):
    raise ValueError('Не все переменные окружения загружены! Проверьте .env файл.')