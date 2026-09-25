import re

import allure
from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage
from config import BASE_URL
from selenium.webdriver.support import expected_conditions as EC


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

    @allure.step("Сортировать: {value}")
    def sort_by(self, value: str):
        # 1. Открыть dropdown сортировки
        button = self.wait_visible(self.SORT_DROPDOWN_BUTTON)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        self.browser.execute_script("arguments[0].click();", button)

        # 2. Кликнуть по нужному пункту
        item = self.wait_visible((
            By.CSS_SELECTOR,
            f".products-sort-order .dropdown-menu a[href*='order={value}']"
        ))
        self.browser.execute_script("arguments[0].click();", item)

        # 3. Дождаться, что URL обновился
        self.wait.until(lambda d: f"order={value}" in d.current_url)

        # 4. Дождаться, что товары отрисовались
        self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#js-product-list article.product-miniature"
        )))

        # 5. ПРОСКРОЛЛИТЬ К СПИСКУ ТОВАРОВ (после перезагрузки viewport сбрасывается наверх)
        self.browser.execute_script(
            "document.querySelector('#js-product-list')"
            ".scrollIntoView({block: 'start'});"
        )
        return self

    @allure.step("Получить список названий товаров")
    def get_names(self) -> list:
        # гарантируем, что все товары видны
        self.browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # небольшая пауза, чтобы DOM устоялся
        import time;
        time.sleep(0.5)

        elements = self.browser.find_elements(*self.PRODUCT_NAME)
        names = []
        for el in elements:
            try:
                txt = el.text.strip()
                if txt:
                    names.append(txt)
            except Exception:
                pass
        allure.attach(str(names), "names", allure.attachment_type.TEXT)
        return names

    @allure.step("Получить список цен товаров")
    def get_prices(self) -> list:
        elements = self.browser.find_elements(*self.PRODUCT_PRICE)
        prices = []
        for el in elements:
            try:
                text = el.text.strip()
                num = re.sub(r"[^\d.,]", "", text).replace(",", ".")
                if num:
                    prices.append(float(num))
            except Exception:
                pass
        allure.attach(str(prices), "prices", allure.attachment_type.TEXT)
        return prices

