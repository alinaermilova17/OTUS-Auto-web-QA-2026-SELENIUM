from tests_selenium.page_objects.login_page import LoginPage
from tests_selenium.page_objects.register_page import RegisterPage
from tests_selenium.page_objects.main_page import MainPage
from tests_selenium.page_objects.product_page import ProductPage
from tests_selenium.page_objects.catalog_page import CatalogPage
from config import BASE_URL


def test_login_page(browser):
    login_page = LoginPage(browser)
    login_page.open(f'{BASE_URL}/login')
    login_page.find(LoginPage.LOGIN_BUTTON)
    login_page.find(LoginPage.EMAIL_INPUT)
    login_page.find(LoginPage.PASSWORD_INPUT)
    login_page.find(LoginPage.FORGOTTEN_PASSWORD)
    login_page.find(LoginPage.SIGNIN_LINK)


def test_main_page(browser):
    main_page = MainPage(browser)
    main_page.open(BASE_URL)
    main_page.find(MainPage.CURRENCY_SELECTOR)
    main_page.find(MainPage.EXPAND_ICON)
    main_page.find(MainPage.CURRENCY_BUTTON)
    main_page.find(MainPage.USD_PRICE)
    main_page.find(MainPage.CONTACT_LINK)


def test_register_page(browser):
    register_page = RegisterPage(browser)
    register_page.open(f'{BASE_URL}/login?create_account=1')
    register_page.find(RegisterPage.REGISTER_FORM)
    register_page.find(RegisterPage.EMAIL_INPUT)
    register_page.find(RegisterPage.PASSWORD_INPUT)
    register_page.find(RegisterPage.FIRSTNAME_INPUT)
    register_page.find(RegisterPage.LASTNAME_INPUT)
    register_page.find(RegisterPage.SAVE_BUTTON)


def test_catalog_page(browser):
    catalog_page = CatalogPage(browser)
    catalog_page.open(f'{BASE_URL}/3-clothes')
    catalog_page.find(CatalogPage.TOP_MENU)
    catalog_page.find(CatalogPage.CATALOG_SEARCH)
    catalog_page.find(CatalogPage.CART_BLOCK)
    catalog_page.find(CatalogPage.SUBCATEGORY_MAN)
    catalog_page.find(CatalogPage.CLOTHES_CATEGORY)


def test_product_page(browser):
    product_page = ProductPage(browser)
    product_page.open(f'{BASE_URL}/men/1-1-hummingbird-printed-t-shirt.html#/1-size-s/8-color-white')
    product_page.find(ProductPage.ADD_TO_CART_BUTTON)
    product_page.find(ProductPage.PRICE_VALUE)
    product_page.find(ProductPage.SIZE_SELECTOR)
    product_page.find(ProductPage.PRODUCT_BANNER)
    product_page.find(ProductPage.PRODUCT_PRICE)


