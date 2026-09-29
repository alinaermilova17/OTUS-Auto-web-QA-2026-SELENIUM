import allure

from tests_selenium.page_objects.login_page import LoginPage
from tests_selenium.page_objects.register_page import RegisterPage
from tests_selenium.page_objects.main_page import MainPage
from tests_selenium.page_objects.product_page import ProductPage
from tests_selenium.page_objects.catalog_page import CatalogPage
from config import BASE_URL


@allure.epic("Интернет-магазин")
@allure.feature("UI Elements")
class TestPageElements:

    @allure.story("Страница логина")
    @allure.title("Проверка элементов на странице логина")
    @allure.description(
        "Открываем страницу /login и проверяем, что на ней присутствуют "
        "кнопка логина, поля email и пароль, ссылка «Забыли пароль» и "
        "ссылка регистрации."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "elements", "login", "smoke")
    def test_login_page(self, browser):
        with allure.step("Открываем страницу логина"):
            login_page = LoginPage(browser)
            login_page.open(f"{BASE_URL}/login")

        with allure.step("Проверяем наличие элементов на странице"):
            login_page.find(LoginPage.LOGIN_BUTTON)
            login_page.find(LoginPage.EMAIL_INPUT)
            login_page.find(LoginPage.PASSWORD_INPUT)
            login_page.find(LoginPage.FORGOTTEN_PASSWORD)
            login_page.find(LoginPage.SIGNIN_LINK)

    @allure.story("Главная страница")
    @allure.title("Проверка элементов на главной странице")
    @allure.description(
        "Открываем главную страницу и проверяем наличие селектора валюты, "
        "кнопки раскрытия, кнопки валюты, цены в USD и ссылки на контакты."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "elements", "main", "smoke")
    def test_main_page(self, browser):
        with allure.step("Открываем главную страницу"):
            main_page = MainPage(browser)
            main_page.open(BASE_URL)

        with allure.step("Проверяем наличие элементов на странице"):
            main_page.find(MainPage.CURRENCY_SELECTOR)
            main_page.find(MainPage.EXPAND_ICON)
            main_page.find(MainPage.CURRENCY_BUTTON)
            main_page.find(MainPage.USD_PRICE)
            main_page.find(MainPage.CONTACT_LINK)

    @allure.story("Страница регистрации")
    @allure.title("Проверка элементов на странице регистрации")
    @allure.description(
        "Открываем страницу регистрации и проверяем наличие формы, полей "
        "email, пароля, имени, фамилии и кнопки сохранения."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "elements", "register", "smoke")
    def test_register_page(self, browser):
        with allure.step("Открываем страницу регистрации"):
            register_page = RegisterPage(browser)
            register_page.open(f"{BASE_URL}/login?create_account=1")

        with allure.step("Проверяем наличие элементов формы регистрации"):
            register_page.find(RegisterPage.REGISTER_FORM)
            register_page.find(RegisterPage.EMAIL_INPUT)
            register_page.find(RegisterPage.PASSWORD_INPUT)
            register_page.find(RegisterPage.FIRSTNAME_INPUT)
            register_page.find(RegisterPage.LASTNAME_INPUT)
            register_page.find(RegisterPage.SAVE_BUTTON)

    @allure.story("Страница каталога")
    @allure.title("Проверка элементов на странице каталога")
    @allure.description(
        "Открываем страницу каталога одежды и проверяем наличие верхнего "
        "меню, поиска, блока корзины, подкатегории «Мужчины» и категории "
        "«Одежда»."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "elements", "catalog", "smoke")
    def test_catalog_page(self, browser):
        with allure.step("Открываем страницу каталога"):
            catalog_page = CatalogPage(browser)
            catalog_page.open(f"{BASE_URL}/3-clothes")

        with allure.step("Проверяем наличие элементов на странице"):
            catalog_page.find(CatalogPage.TOP_MENU)
            catalog_page.find(CatalogPage.CATALOG_SEARCH)
            catalog_page.find(CatalogPage.CART_BLOCK)
            catalog_page.find(CatalogPage.SUBCATEGORY_MAN)
            catalog_page.find(CatalogPage.CLOTHES_CATEGORY)

    @allure.story("Страница товара")
    @allure.title("Проверка элементов на странице товара")
    @allure.description(
        "Открываем страницу товара и проверяем наличие кнопки «Добавить в "
        "корзину», цены, селектора размера, баннера товара и блока цены."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "elements", "product", "smoke")
    def test_product_page(self, browser):
        with allure.step("Открываем страницу товара"):
            product_page = ProductPage(browser)
            product_page.open(
                f"{BASE_URL}/men/1-1-hummingbird-printed-t-shirt.html"
                f"#/1-size-s/8-color-white"
            )

        with allure.step("Проверяем наличие элементов на странице"):
            product_page.find(ProductPage.ADD_TO_CART_BUTTON)
            product_page.find(ProductPage.PRICE_VALUE)
            product_page.find(ProductPage.SIZE_SELECTOR)
            product_page.find(ProductPage.PRODUCT_BANNER)
            product_page.find(ProductPage.PRODUCT_PRICE)