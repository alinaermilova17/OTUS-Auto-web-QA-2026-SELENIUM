import allure
from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage
from config import BASE_URL



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
    SORT_DROPDOWN_BUTTON = (By.CSS_SELECTOR,"#js-product-list-top > div:nth-child(2) > div > " "div.products-sort-order.dropdown > button")
    SORT_OPTION_NAME_DESC = (By.CSS_SELECTOR, ".products-sort-order .dropdown-menu a[href*='name.desc']")


    @allure.step("Нажать на подкатегорию 'Men'")
    def subcategory_men(self):
        self.click(self.SUBCATEGORY_MAN)
        return self


    @allure.step("Открыть категорию Art")
    def open_art_category(self):
        self.click(self.ART_MENU)
        return self

    @allure.step("Открыть категорию Art по URL")
    def open_art_by_url(self):
        self.browser.get(f'{BASE_URL}/9-art')
        return self

    @allure.step("Выбрать сортировку: Z-A")
    def sort_by(self):
        self.click(self.SORT_DROPDOWN_BUTTON)
        self.click(self.SORT_OPTION_NAME_DESC)
        return self



    @allure.step("Получить список названий товаров")
    def get_names(self) -> list:
        elements = self.browser.find_elements(*self.PRODUCT_NAME)
        names = [el.text.strip() for el in elements if el.text.strip()]
        allure.attach(str(names), "names", allure.attachment_type.TEXT)
        return names