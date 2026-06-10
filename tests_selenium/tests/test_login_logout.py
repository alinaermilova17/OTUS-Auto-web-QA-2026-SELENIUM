import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests_selenium.pages.catalog_page import CatalogPage
from tests_selenium.pages.login_page import LoginPage

load_dotenv()

base_url = "http://localhost:8080"


def test_login_logout(browser):
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

    account_button = browser.find_element(*LoginPage.ACCOUNT_LINK)
    account_button.click()

    logout_button = browser.find_element(*LoginPage.LOGOUT_BUTTON)
    logout_button.click()




