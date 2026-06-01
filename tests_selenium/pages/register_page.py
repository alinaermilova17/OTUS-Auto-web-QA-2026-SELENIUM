from selenium.webdriver.common.by import By


class RegisterPage:
    FIRSTNAME_INPUT = (By.ID, "field-firstname")
    LASTNAME_INPUT = (By.ID, "field-lastname")
    EMAIL_INPUT = (By.ID, "field-email")
    PASSWORD_INPUT = (By.ID, "field-password")
    REGISTER_FORM = (By.CSS_SELECTOR, "#content > section")
    SAVE_BUTTON = (By.CSS_SELECTOR, "#customer-form > footer > button")

