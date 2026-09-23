import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage


class WishlistPage(BasePage):
    CLOTHES_MENU = (By.XPATH, "//li[@id='category-3']//a[contains(@class,'dropdown-item')]")
    WOMEN_LINK   = (By.XPATH, "//ul[contains(@class,'category-sub-menu')]//a[normalize-space()='Women']")
    PRODUCT_BROWN_BEAR = (    By.XPATH,
    "//h3[contains(@class,'product-title')]//a[contains(text(),'Brown bear printed sweater')]"
)
    PRODUCT_TITLE   = (By.CSS_SELECTOR, "h1.h1")
    WISHLIST_BUTTON = (By.CSS_SELECTOR, "button.wishlist-button-add")
    WISHLIST_ICON   = (By.CSS_SELECTOR, "button.wishlist-button-add i")
    WISHLIST_TOAST  = (By.CSS_SELECTOR, ".wishlist-toast.success")

    MY_WISHLIST_LINK = (By.CSS_SELECTOR, "a[title='My wishlists'], a[href*='blockwishlist']")
    WISHLIST_ITEM    = (By.CSS_SELECTOR, ".wishlist-list-item-title, .wishlist-list-item")

    @allure.step("Открыть категорию Clothes → Women")
    def open_women_category(self):
        self.click(self.CLOTHES_MENU)
        self.click(self.WOMEN_LINK)
        return self

    @allure.step("Открыть карточку 'Brown bear printed sweater'")
    def open_brown_bear_product(self):
        self.click(self.PRODUCT_BROWN_BEAR)
        return self

    @allure.step("Добавить текущий товар в wishlist")
    def add_to_wishlist(self):
        button = self.wait_visible(self.WISHLIST_BUTTON, timeout=15)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button
        )
        ActionChains(self.browser).move_to_element(button).perform()
        button.click()
        return self

    @allure.step("Переключить состояние wishlist (toggle)")
    def toggle_wishlist(self):
        self.click(self.WISHLIST_ICON)
        return self

    @allure.step("Дождаться тоста 'Product added'")
    def wait_for_added_toast(self):
        self.wait_visible(self.WISHLIST_TOAST, timeout=15)
        return self

    @allure.step("Открыть 'My wishlist'")
    def open_my_wishlist(self):
        self.click(self.MY_WISHLIST_LINK)
        self.click(self.WISHLIST_ITEM)
        return self

    @allure.step("Проверить, что открыт товар '{title}'")
    def is_product_opened(self, title: str) -> bool:
        el = self.wait_visible(self.PRODUCT_TITLE, timeout=15)
        return title.lower() in el.text.lower()

    @allure.step("Проверить, что товар '{title}' есть в wishlist")
    def has_product(self, title: str) -> bool:
        locator = (By.CSS_SELECTOR, f"img[title='{title}']")
        return self.is_visible(locator)

    @allure.step("Проверить, что иконка wishlist в состоянии 'favorite_border'")
    def is_wishlist_icon_border(self) -> bool:
        icon = self.find(self.WISHLIST_ICON)
        cls = icon.get_attribute("class") or ""
        return "favorite_border" in cls