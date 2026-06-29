from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    MY_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[title='View my customer account']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a[href*='logout']")

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 15)

    def is_user_logged_in(self) -> bool:
        return len(self.browser.find_elements(*self.MY_ACCOUNT_LINK)) > 0

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON)).click()
