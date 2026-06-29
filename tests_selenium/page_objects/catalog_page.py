from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class CatalogPage:
    CATALOG_MENU = (By.CSS_SELECTOR, '_desktop_top_menu')
    MOBILE_CART = (By.CSS_SELECTOR,  '_mobile_cart > div')
    BLOCK_CATEGORY = (By.CSS_SELECTOR, 'js-product-list-header > div')
    CATALOG_SEARCH = (By.CSS_SELECTOR, 'search_widget > form > input.ui-autocomplete-input')
    SUBCATEGORY_MAN = (By.XPATH, "//a[text()='Men']")
    CLOTHES_CATEGORY = (By.XPATH, "//a[contains(text(), 'Clothes')]")

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    def subcategory_men(self):
        self.browser.find_element(*CatalogPage.SUBCATEGORY_MAN).click()