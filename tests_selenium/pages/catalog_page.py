from selenium.webdriver.common.by import By


class CatalogPage:
    CATALOG_MENU = (By.CSS_SELECTOR, "_desktop_top_menu")
    MOBILE_CART = (By.CSS_SELECTOR,  "_mobile_cart > div")
    BLOCK_CATEGORY = (By.CSS_SELECTOR, "js-product-list-header > div")
    CATALOG_SEARCH = (By.CSS_SELECTOR, "search_widget > form > input.ui-autocomplete-input")
    SUBCATEGORY_MAN = (By.XPATH, "//a[text()='Men']")
    CLOTHES_CATEGORY = (By.XPATH, "//a[contains(text(), 'Clothes')]")