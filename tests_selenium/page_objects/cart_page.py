from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR,
                          'add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > div.add > button')
    QUANTITY = (By.XPATH, "//div[contains(@class, 'qty')]//input[@type='number']")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "img[alt='Hummingbird printed t-shirt']")
    ADD_TO_CART_FROM_MAIN_PAGE = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
    ITEM_TO_CART = (By.CSS_SELECTOR, '.cart-products-count')
    CART_ITEM = (By.CSS_SELECTOR, '.cart-products-count')
    MODAL_WIDOW_CLOSE_BUTTON = (By.XPATH, "//div[@id='blockcart-modal']//button[@data-dismiss='modal']/span/i")
    CART_LABEL = (By.CSS_SELECTOR, '#_desktop_cart .hidden-sm-down')
    DELETE_BUTTON = (By.CSS_SELECTOR, "a[data-link-action='delete-from-cart']")
    SUBTOTAL_ZERO_CHECK = (By.CSS_SELECTOR, '#cart-subtotal-products .label.js-subtotal')

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    def add_to_cart(self):
        self.browser.find_element(*self.PRODUCT_IMAGE).click()
        self.browser.find_element(*self.ADD_TO_CART_FROM_MAIN_PAGE).click()

    def close_cart_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.MODAL_WIDOW_CLOSE_BUTTON)).click()

    def open_cart(self):
        self.browser.find_element(*self.CART_LABEL).click()

    def is_product_in_cart(self):
        assert self.browser.find_element(*self.ITEM_TO_CART).is_displayed()

    def get_current_quantity(self) -> int:
        qty_input = self.browser.find_element(*self.QUANTITY)
        return int(qty_input.get_attribute('value'))

    def delete_from_cart(self):
        self.browser.find_element(*self.DELETE_BUTTON).click()

    def is_cart_empty_by_subtotal(self):
        try:
            element = self.browser.find_element(*self.SUBTOTAL_ZERO_CHECK)
            text = element.text.strip().lower()
            return '0' in text
        except:
            return False

