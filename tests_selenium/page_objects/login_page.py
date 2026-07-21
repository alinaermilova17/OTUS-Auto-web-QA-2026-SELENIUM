import allure
from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, 'field-email')
    PASSWORD_INPUT = (By.ID, 'field-password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FORGOTTEN_PASSWORD = (By.LINK_TEXT, "Forgot your password?")
    SIGNIN_LINK = (By.CSS_SELECTOR, "a[title='Log in to your customer account']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '#_desktop_user_info > div > a.logout.hidden-sm-down ')
    MY_ACCOUNT_HEADER = (By.LINK_TEXT, 'Your account')
    ACCOUNT_LINK = (By.CSS_SELECTOR, '#_desktop_user_info > div > a.account')

    @allure.step("Ввести имейл: {email}")
    def enter_email(self, email: str):
        return self.wait_visible(self.EMAIL_INPUT).send_keys(email)

    @allure.step("Ввести пароль: {password}")
    def enter_password(self, password: str):
        return self.find(self.PASSWORD_INPUT).send_keys(password)

    @allure.step("Кликнуть кнопку логина")
    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    @allure.step("Залогинить пользователя")
    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self