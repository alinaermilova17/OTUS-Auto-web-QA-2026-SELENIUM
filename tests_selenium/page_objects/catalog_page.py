import allure
from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage


class CatalogPage(BasePage):
    TOP_MENU = (By.XPATH, "//div[@id='_desktop_top_menu']")
    CART_BLOCK = (By.CSS_SELECTOR, '#_desktop_cart')
    CATALOG_SEARCH = (By.CSS_SELECTOR, '#search_widget input')
    SUBCATEGORY_MAN = (By.XPATH, "//a[text()='Men']")
    CLOTHES_CATEGORY = (By.XPATH, "//div[@class='block-categories']")

    @allure.step("Нажать на подкатегорию 'Men'")
    def subcategory_men(self):
        self.click(self.SUBCATEGORY_MAN)
        return self