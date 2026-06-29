import os
from dotenv import load_dotenv
from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.main_page import MainPage
from tests_selenium.page_objects.login_page import LoginPage

load_dotenv()


def test_switch_currency_main_page(browser):
    email = os.getenv('login')
    password = os.getenv('password')
    base_url = os.getenv('base_url')

    login_page = LoginPage(browser)
    home_page = HomePage(browser)
    main_page = MainPage(browser)
    login_page.open(base_url).login(email, password)

    assert home_page.is_user_logged_in()

    main_page.currency_usd_switch()
    main_page.price_in_usd()