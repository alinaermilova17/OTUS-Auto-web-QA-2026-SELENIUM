import allure

from config import BASE_URL, LOGIN, PASSWORD
from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.catalog_page import CatalogPage
from tests_selenium.page_objects.main_page import MainPage
from tests_selenium.page_objects.login_page import LoginPage


@allure.epic("Интернет-магазин")
@allure.feature("Валюта")
class TestCurrency:

    @allure.story("Переключение валюты")
    @allure.title("Проверка переключения валют в каталоге")
    @allure.description(
        "Авторизуемся, переключаем валюту на USD, открываем категорию "
        "Clothes → Men и проверяем, что цены в каталоге отображаются в USD."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "currency", "catalog")
    def test_switch_currency_catalog(self, browser):
        with allure.step("Авторизуемся в системе"):
            login_page = LoginPage(browser)
            login_page.open(f"{BASE_URL}/login")
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Проверяем, что пользователь авторизован"):
            home_page = HomePage(browser)
            assert home_page.is_user_logged_in(), "Пользователь не авторизован"

        with allure.step("Переключаем валюту на USD"):
            main_page = MainPage(browser)
            main_page.currency_usd_switch()

        with allure.step("Открываем категорию Clothes"):
            main_page.open(f"{BASE_URL}/3-clothes")

        with allure.step("Переходим в подкатегорию Men"):
            catalog_page = CatalogPage(browser)
            catalog_page.subcategory_men()

        with allure.step("Проверяем, что цены отображаются в USD"):
            main_page.price_in_usd()
