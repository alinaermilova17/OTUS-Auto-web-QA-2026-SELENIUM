import logging
import os
import time
from dotenv import load_dotenv
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.register_page import RegisterPage

logger = logging.getLogger(__name__)
load_dotenv()
fake = Faker('en_US')


def generate_user_data():
    return {
        'firstname': fake.first_name(),
        'lastname': fake.last_name(),
        'email': fake.email(),
        'password': fake.password(length=10, special_chars=True, digits=True, upper_case=True),
        'birthdate': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%m/%d/%Y')
    }


def test_register_page(browser):
    base_url = os.getenv('base_url')
    user_data = generate_user_data()
    logger.info(" Регистрация пользователя: {user_data['email']}")

    register_page = RegisterPage(browser)
    register_page.open_register_form(base_url)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )


    logger.info(' Заполнение формы регистрации...')
    register_page.register(user_data)
    logger.info(' Форма отправлена')

    save_user_data(user_data)

    home_page = HomePage(browser)
    logger.info(' Ожидание завершения регистрации...')
    WebDriverWait(browser, 10).until(
        EC.url_changes(browser.current_url)
    )
    time.sleep(2)
    logger.info(' Регистрация завершена')

    if home_page.is_user_logged_in():
        logger.info(' Пользователь успешно залогинен!')
        logger.info(f" ТЕСТ ПРОЙДЕН: Пользователь {user_data['email']} зарегистрирован")
    else:
        logger.error(' Пользователь не залогинен после регистрации')
        assert False, ' Пользователь не залогинен после регистрации'

def save_user_data(user_data):
    import json
    with open('test_user_data.json', 'w') as f:
        json.dump(user_data, f, indent=2)


def load_user_data():
    import json
    try:
        with open('test_user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None