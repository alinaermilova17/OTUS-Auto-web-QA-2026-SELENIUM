import allure
from tests_selenium.page_objects.login_page import LoginPage
from config import LOGIN, PASSWORD, BASE_URL

@allure.feature("Login / Demo failure")
class TestLoginFailDemo:

    @allure.title("Логин падает — демонстрация скриншота в Allure")
    def test_login_fails_and_screenshot(self, browser):
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(browser)
            login_page.open(f"{BASE_URL}/login")

        with allure.step("Проверить несуществующий элемент на странице логина"):
            browser.find_element(
                "css selector",
                "#button-that-does-not-exist-on-login-page-12345"
            )

        with allure.step("Проверить, что пользователь залогинен"):
            assert False, "Этот шаг не должен выполниться"