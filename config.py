import os
from dotenv import load_dotenv

load_dotenv()


LOGIN = os.getenv('login')
PASSWORD = os.getenv('password')
BASE_URL = os.getenv('base_url', 'http://prestashop:80')

if not all([LOGIN, PASSWORD, BASE_URL]):
    raise ValueError('Не все переменные окружения загружены! Проверьте .env файл.')