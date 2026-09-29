import allure

from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.login_page import LoginPage
from config import LOGIN, PASSWORD, BASE_URL


@allure.epic("Интернет-магазин")
@allure.feature("Авторизация")
class TestLoginLogout:

    @allure.story("Login / Logout")
    @allure.title("Проверка логина и последующего логаута")
    @allure.description(
        "Авторизуемся с валидными кредами, проверяем что пользователь "
        "залогинен, затем выполняем logout и проверяем, что пользователь "
        "вышел из системы."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "auth", "login", "logout", "smoke")
    def test_login_logout(self, browser):
        with allure.step("Открываем страницу логина"):
            login_page = LoginPage(browser)
            login_page.open(f"{BASE_URL}/login")

        with allure.step("Авторизуемся с валидными кредами"):
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Проверяем, что пользователь авторизован"):
            home_page = HomePage(browser)
            assert home_page.is_user_logged_in(), "Пользователь не авторизован"

        with allure.step("Выполняем logout"):
            home_page.logout()

        with allure.step("Проверяем, что пользователь вышел из системы"):
            assert not home_page.is_user_logged_in(), (
                "Пользователь остался авторизованным после logout"
            )