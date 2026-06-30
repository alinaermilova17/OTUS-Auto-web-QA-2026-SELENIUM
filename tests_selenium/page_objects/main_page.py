from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage


class MainPage(BasePage):
    MOBILE_CART = (By.CSS_SELECTOR, '_mobile_cart > div')
    CONTACT_LINK = (By.CSS_SELECTOR, '#contact-link')
    CURRENCY_SELECTOR = (By.CSS_SELECTOR, '.expand-more._gray-darker')
    USD_OPTION = (By.CSS_SELECTOR, "a[title='US Dollar']")
    EXPAND_ICON = (By.CSS_SELECTOR, 'i.material-icons.expand-more')
    CURRENCY_BUTTON = (By.CSS_SELECTOR, '.expand-more._gray-darker')
    USD_PRICE = (By.CSS_SELECTOR, "span.price[aria-label='Price']")

    def currency_usd_switch(self):
        self.find(MainPage.CURRENCY_BUTTON).click()
        self.wait_visible(MainPage.USD_OPTION)
        self.find(MainPage.USD_OPTION).click()

    def price_in_usd(self):
        price_text = self.find(MainPage.USD_PRICE).text
        assert "$" in price_text, f"Цена не в долларах: {price_text}"