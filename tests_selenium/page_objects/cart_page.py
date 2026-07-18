import allure
from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage


class CartPage(BasePage):
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

    @allure.step('Добавить продукт в корзину')
    def add_to_cart(self):
        self.find(self.PRODUCT_IMAGE).click()
        self.find(self.ADD_TO_CART_FROM_MAIN_PAGE).click()

    @allure.step('Закрыть модальное окно корзины')
    def close_cart_modal(self):
        return self.click(self.MODAL_WIDOW_CLOSE_BUTTON)

    @allure.step('Перейти к корзине')
    def open_cart(self):
        return self.click(self.CART_LABEL)

    @allure.step('Продукт находится в корзине')
    def is_product_in_cart(self):
        return self.is_visible(self.ITEM_TO_CART)

    @allure.step('Проверить текущее количество в корзине')
    def get_current_quantity(self) -> int:
        quantity = self.get_attribute(self.QUANTITY, 'value')
        return int(quantity)

    @allure.step('Удалить продукт из корзины')
    def delete_from_cart(self):
        return self.find(self.DELETE_BUTTON).click()

    @allure.step('Корзина пуста')
    def is_cart_empty_by_subtotal(self):
        try:
            element = self.find(self.SUBTOTAL_ZERO_CHECK)
            text = element.text.strip().lower()
            return '0' in text
        except:
            return False

