import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests_selenium.pages.login_page import LoginPage
from tests_selenium.pages.product_page import ProductPage

load_dotenv()

base_url = "http://localhost:8080"


def test_add_to_cart(browser):
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

    add_product = browser.find_element(*ProductPage.PRODUCT_IMAGE)
    add_product.click()

    add_button = browser.find_element(*ProductPage.ADD_TO_CART_FROM_MAIN_PAGE)
    add_button.click()

    item_to_cart = browser.find_element(*ProductPage.ITEM_TO_CART)
    assert item_to_cart.is_displayed()