from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests_selenium.pages.login_page import LoginPage
from tests_selenium.pages.register_page import RegisterPage
from tests_selenium.pages.main_page import MainPage
from tests_selenium.pages.product_page import ProductPage
from tests_selenium.pages.catalog_page import CatalogPage


base_url = "http://localhost:8080"


def test_login_page(browser):
    browser.get(f'{base_url}/login?back=http%3A%2F%2Flocalhost%3A8080%2F')
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    browser.find_elements(*LoginPage.LOGIN_BUTTON)
    browser.find_elements(*LoginPage.EMAIL)
    browser.find_elements(*LoginPage.PASSWORD)
    browser.find_elements(*LoginPage.FORGOTTEN_PASSWORD)
    browser.find_elements(*LoginPage.SIGNIN_LINK)


def test_main_page(browser):
    browser.get(f'{base_url}')
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    browser.find_elements(*MainPage.USER_BUTTON)
    browser.find_elements(*MainPage.SUBSCRIBE_BUTTON)
    browser.find_elements(*MainPage.MOBILE_CART)
    browser.find_elements(*MainPage.DESKTOP_LOGO)
    browser.find_elements(*MainPage.SEARCH_FIELD)


def test_register_page(browser):
    browser.get(f'{base_url}/registration')
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    browser.find_elements(*RegisterPage.REGISTER_FORM)
    browser.find_elements(*RegisterPage.EMAIL_INPUT)
    browser.find_elements(*RegisterPage.PASSWORD_INPUT)
    browser.find_elements(*RegisterPage.FIRSTNAME_INPUT)
    browser.find_elements(*RegisterPage.LASTNAME_INPUT)
    browser.find_elements(*RegisterPage.SAVE_BUTTON)


def test_catalog_page(browser):
    browser.get(f'{base_url}/3-clothes')
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    browser.find_elements(*CatalogPage.CATALOG_MENU)
    browser.find_elements(*CatalogPage.CATALOG_SEARCH)
    browser.find_elements(*CatalogPage.MOBILE_CART)
    browser.find_elements(*CatalogPage.SUBCATEGORY_MAN)
    browser.find_elements(*CatalogPage.BLOCK_CATEGORY)


def test_product_page(browser):
    browser.get(f'{base_url}/men/1-1-hummingbird-printed-t-shirt.html#/1-size-s/8-color-white')
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )
    browser.find_elements(*ProductPage.PRODUCT_BANNER)
    browser.find_elements(*ProductPage.NAME)
    browser.find_elements(*ProductPage.SIZE)
    browser.find_elements(*ProductPage.QUANTITY)
    browser.find_elements(*ProductPage.ADD_TO_CART_BUTTON)


