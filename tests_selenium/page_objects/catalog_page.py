import allure
from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage
from selenium.webdriver.support.ui import Select
import re


class CatalogPage(BasePage):
    TOP_MENU = (By.XPATH, "//div[@id='_desktop_top_menu']")
    CART_BLOCK = (By.CSS_SELECTOR, '#_desktop_cart')
    CATALOG_SEARCH = (By.CSS_SELECTOR, '#search_widget input')
    SUBCATEGORY_MAN = (By.XPATH, "//a[text()='Men']")
    CLOTHES_CATEGORY = (By.XPATH, "//div[@class='block-categories']")
    ART_MENU = (By.CSS_SELECTOR, "a.dropdown-item[href*='/9-art']")
    SORT_SELECT = (By.CSS_SELECTOR, "select.product-sort, select[name='orderby']")
    PRODUCTS = (By.CSS_SELECTOR, "#js-product-list article.product-miniature")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".price, span[itemprop='price']")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-title a, h3.product-title a, h2.product-title a")

    @allure.step("Нажать на подкатегорию 'Men'")
    def subcategory_men(self):
        self.click(self.SUBCATEGORY_MAN)
        return self


    @allure.step("Открыть категорию Art")
    def open_art_category(self):
        self.click(self.ART_MENU)
        return self

    @allure.step("Открыть категорию Art по URL")
    def open_art_by_url(self,url):
        self.browser.get(url)
        return self

    @allure.step("Выбрать сортировку: {value}")
    def sort_by(self, value: str):
        select_el = self.wait_visible(self.SORT_SELECT)
        Select(select_el).select_by_value(value)
        self.wait.until(
            lambda d: value in d.current_url or "orderby" in d.current_url
        )
        return self

    @allure.step("Получить список цен товаров")
    def get_prices(self) -> list:
        elements = self.browser.find_elements(*self.PRODUCT_PRICE)
        prices = []
        for el in elements:
            text = el.text.strip()
            num = re.sub(r"[^\d.,]", "", text).replace(",", ".")
            if num:
                try:
                    prices.append(float(num))
                except ValueError:
                    pass
        allure.attach(
            str(prices), "prices", allure.attachment_type.TEXT
        )
        return prices

    @allure.step("Получить список названий товаров")
    def get_names(self) -> list:
        elements = self.browser.find_elements(*self.PRODUCT_NAME)
        names = [el.text.strip() for el in elements if el.text.strip()]
        allure.attach(str(names), "names", allure.attachment_type.TEXT)
        return names