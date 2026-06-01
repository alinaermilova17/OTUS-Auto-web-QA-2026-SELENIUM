from selenium.webdriver.common.by import By


class ProductPage:
    PRODUCT_BANNER = (By.CSS_SELECTOR, "img[alt='Hummingbird printed t-shirt']")
    NAME = (By.CSS_SELECTOR, "main > div.row.product-container.js-product-container > div:nth-child(2) > h1")
    SIZE = (By.CSS_SELECTOR, "group_1")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > div.add > button")
    QUANTITY= (By.NAME, "qty")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "img[alt='Hummingbird printed t-shirt']")
    ADD_TO_CART_FROM_MAIN_PAGE = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
    ITEM_TO_CART = (By.CSS_SELECTOR, ".cart-products-count")

