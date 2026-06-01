import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests_selenium.pages.catalog_page import CatalogPage
from tests_selenium.pages.main_page import MainPage
from tests_selenium.pages.login_page import LoginPage

load_dotenv()

base_url = "http://localhost:8080"


def test_switch_currency_calatalog(browser):
    login = os.getenv("login")
    password = os.getenv("password")
    browser.get(f"{base_url}/login")
    wait = WebDriverWait(browser, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    email_input = wait.until(
        EC.visibility_of_element_located(LoginPage.EMAIL)
    )
    email_input.send_keys(login)

    password_input = browser.find_element(*LoginPage.PASSWORD)
    password_input.send_keys(password)

    login_button = browser.find_element(*LoginPage.LOGIN_BUTTON)
    login_button.click()

    currency_button = browser.find_element(*MainPage.CURRENCY_BUTTON)
    currency_button.click()

    wait.until(EC.visibility_of_element_located(MainPage.USD_OPTION))

    usd_option = browser.find_element(*MainPage.USD_OPTION)
    usd_option.click()

    browser.get(f"{base_url}/3-clothes")

    subcategory = browser.find_element(*CatalogPage.SUBCATEGORY_MAN)
    subcategory.click()

    price_text = browser.find_element(*MainPage.USD_PRICE).text
    assert "$" in price_text, f"Цена не в долларах: {price_text}"

