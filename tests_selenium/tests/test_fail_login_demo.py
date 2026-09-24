import allure
from tests_selenium.page_objects.login_page import LoginPage
from config import LOGIN, PASSWORD, BASE_URL

@allure.feature("Login / Demo failure")
class TestLoginFailDemo:

    @allure.title("Логин падает — демонстрация скриншота в Allure")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Принудительное падение на логине")
    def test_login_fails_and_screenshot(self, browser):
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(browser)
            login_page.open(f"{BASE_URL}/login")

        with allure.step("Проверить несуществующий элемент на странице логина"):
            # Ищем кнопку, которой на странице логина точно нет.
            # Selenium подождёт 15 секунд и упадёт с NoSuchElementException.
            # conftest.py hook прикрепит скриншот именно этой страницы.
            browser.find_element(
                "css selector",
                "#button-that-does-not-exist-on-login-page-12345"
            )

        # Сюда выполнение не дойдёт
        with allure.step("Проверить, что пользователь залогинен"):
            assert False, "Этот шаг не должен выполниться"