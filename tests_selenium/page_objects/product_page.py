from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:
    PRODUCT_NAME = (By.CSS_SELECTOR, 'h1.h1')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '.current-price span')
    PRODUCT_BANNER = (By.CSS_SELECTOR, "img[alt='Hummingbird printed t-shirt']")
    NAME = (By.CSS_SELECTOR, 'main > div.row.product-container.js-product-container > div:nth-child(2) > h1')
    SIZE = (By.CSS_SELECTOR, 'group_1')
    PRODUCT_NAME_IN_CART = (By.CSS_SELECTOR, '.product-line-info a')

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)


    def get_product_name(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.PRODUCT_NAME)).text

