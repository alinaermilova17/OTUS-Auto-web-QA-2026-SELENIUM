from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, timeout=10):
        self.browser = browser
        self.wait = WebDriverWait(browser, timeout)

    def open(self, url):
        return self.browser.get(url)

    def find(self, locator):
        return self.browser.find_element(*locator)

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.wait_clickable(locator).click()

    def get_attribute(self, locator, attribute_name):
        return self.wait_visible(locator).get_attribute(attribute_name)

    def is_visible(self, locator) -> bool:
        return self.wait_visible(locator).is_displayed()
