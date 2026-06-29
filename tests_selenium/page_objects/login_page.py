from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    EMAIL_INPUT = (By.ID, 'field-email')
    PASSWORD_INPUT = (By.ID, 'field-password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FORGOTTEN_PASSWORD = (By.LINK_TEXT, "Forgot your password?")
    SIGNIN_LINK = (By.CSS_SELECTOR, "a[title='Log in to your customer account']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '#_desktop_user_info > div > a.logout.hidden-sm-down ')
    MY_ACCOUNT_HEADER = (By.LINK_TEXT, 'Your account')
    ACCOUNT_LINK = (By.CSS_SELECTOR, '#_desktop_user_info > div > a.account')

    def __init__(self, browser):
        self.browser= browser
        self.wait = WebDriverWait(browser, 15)

    def open(self, base_url: str):
        self.browser.get(f'{base_url}/login')
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        return self

    def enter_email(self, email: str):
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).send_keys(email)
        return self

    def enter_password(self, password: str):
        self.browser.find_element(*self.PASSWORD_INPUT).send_keys(password)
        return self

    def click_login(self):
        self.browser.find_element(*self.LOGIN_BUTTON).click()

    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self