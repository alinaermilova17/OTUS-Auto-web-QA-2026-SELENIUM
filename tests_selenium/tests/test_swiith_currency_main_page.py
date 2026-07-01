from config import BASE_URL, LOGIN, PASSWORD
from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.main_page import MainPage
from tests_selenium.page_objects.login_page import LoginPage


def test_switch_currency_main_page(browser):
    login_page = LoginPage(browser)
    home_page = HomePage(browser)
    main_page = MainPage(browser)

    login_page.open(f'{BASE_URL}/login')
    login_page.login(LOGIN, PASSWORD)

    assert home_page.is_user_logged_in()
    main_page.currency_usd_switch()
    main_page.price_in_usd()