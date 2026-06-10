from selenium.webdriver.common.by import By


class LoginPage:
    EMAIL = (By.ID, "field-email")
    PASSWORD = (By.ID, "field-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FORGOTTEN_PASSWORD = (By.LINK_TEXT, "Forgot your password?")
    SIGNIN_LINK = (By.CSS_SELECTOR, "a[title='Log in to your customer account']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "#_desktop_user_info > div > a.logout.hidden-sm-down ")
    MY_ACCOUNT_HEADER = (By.LINK_TEXT,  "Your account")
    ACCOUNT_LINK = (By.CSS_SELECTOR, "#_desktop_user_info > div > a.account")
