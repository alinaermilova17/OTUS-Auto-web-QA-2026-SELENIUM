from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.login_page import LoginPage
from config import LOGIN, PASSWORD, BASE_URL


def test_login_logout(browser):
    login_page = LoginPage(browser)
    home_page = HomePage(browser)
    login_page.open(f'{BASE_URL}/login')
    login_page.login(LOGIN, PASSWORD)

    assert home_page.is_user_logged_in()
    home_page.logout()




