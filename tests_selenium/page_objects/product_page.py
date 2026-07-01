from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_NAME = (By.CSS_SELECTOR, 'h1.h1')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '.current-price span')
    PRODUCT_BANNER = (By.CSS_SELECTOR, "img[alt='Hummingbird printed t-shirt']")
    PRICE_VALUE = (By.CSS_SELECTOR, '.current-price-value')
    SIZE_SELECTOR = (By.CSS_SELECTOR, 'select.form-control#group_1')
    ADD_TO_CART_BUTTON = (By.XPATH, "//*[@id='add-to-cart-or-refresh']//button[@data-button-action='add-to-cart']")

    def get_product_name(self) -> str:
        return self.wait_visible(self.PRODUCT_NAME).text

