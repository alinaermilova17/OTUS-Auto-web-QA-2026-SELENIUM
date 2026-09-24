import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL
from tests_selenium.page_objects.base_page import BasePage


class WishlistPage(BasePage):
    CLOTHES_MENU = (By.XPATH, "//li[@id='category-3']//a[contains(@class,'dropdown-item')]")
    WOMEN_LINK   = (By.XPATH, "//ul[contains(@class,'category-sub-menu')]//a[normalize-space()='Women']")
    PRODUCT_BROWN_BEAR = (By.CSS_SELECTOR,"a[href*='brown-bear-printed-sweater']")
    WISHLIST_BUTTON = (By.CSS_SELECTOR, "button.wishlist-button-add")
    WISHLIST_MODAL = (By.CSS_SELECTOR, ".wishlist-modal.modal.show, .wishlist-modal.modal.fade.show")
    WISHLIST_MODAL_ITEM = (By.CSS_SELECTOR,
        ".wishlist-modal.modal.show .modal-body ul li p, "
        ".wishlist-modal.modal.fade.show .modal-body ul li p")
    MY_WISHLIST_FOOTER   = (By.CSS_SELECTOR, "#footer_account_list > li:nth-child(5) > a")
    WISHLIST_LIST_FIRST  = (By.CSS_SELECTOR, "#content > div > ul > li > a > p")
    WISHLIST_PRODUCT_IMG = (By.CSS_SELECTOR, "#content > ul > li > div > a > div.wishlist-product-image > img")
    WISHLIST_ICON = (By.CSS_SELECTOR, "button.wishlist-button-add i")

    @allure.step("Открыть Clothes → Women")
    def open_women_category(self):
        self.click(self.CLOTHES_MENU)
        self.click(self.WOMEN_LINK)
        return self

    @allure.step("Открыть карточку товара")
    def open_brown_bear_product(self):
        self.click(self.PRODUCT_BROWN_BEAR)
        return self

    @allure.step("Проверить, что открыт товар")
    def is_product_opened(self) -> bool:
        url = self.browser.current_url
        allure.attach(url, "current url", allure.attachment_type.TEXT)
        return "brown-bear-printed-sweater" in url

    def add_to_wishlist(self):
        self.click(self.WISHLIST_BUTTON)

        try:
            self.wait_visible(self.WISHLIST_MODAL, timeout=10)
            item = self.wait_clickable(self.WISHLIST_MODAL_ITEM)
            self.browser.execute_script("arguments[0].click();", item)
            self.wait_invisible(self.WISHLIST_MODAL)
        except Exception as e:
            allure.attach(
                self.browser.get_screenshot_as_png(),
                "modal_not_found",
                allure.attachment_type.PNG
            )
            allure.attach(
                str(e), "exception", allure.attachment_type.TEXT
            )
        return self

    @allure.step("Перейти в My wishlists через футер")
    def open_my_wishlist(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.click(self.MY_WISHLIST_FOOTER)
        return self

    @allure.step("Открыть первый сохранённый wishlist")
    def open_first_wishlist(self):
        self.click(self.WISHLIST_LIST_FIRST)
        return self

    @allure.step("Проверить, что товар есть в wishlist")
    def has_product_in_wishlist(self) -> bool:
        return self.is_visible(self.WISHLIST_PRODUCT_IMG)

    @allure.step("Убедиться, что товар в wishlist")
    def ensure_in_wishlist(self):
        icon = self.find(self.WISHLIST_ICON)
        classes = icon.get_attribute("class") or ""
        allure.attach(classes, "icon class before", allure.attachment_type.TEXT)

        if "favorite_border" in classes:
            # товара нет — добавляем
            allure.attach("adding to wishlist", "action", allure.attachment_type.TEXT)
            self.click(self.WISHLIST_BUTTON)
            self.wait.until(
                lambda d: "favorite_border" not in (
                        d.find_element(*self.WISHLIST_ICON).get_attribute("class") or ""
                )
            )
        else:
            # товар уже в wishlist — ничего не делаем
            allure.attach("already in wishlist", "action", allure.attachment_type.TEXT)

        return self

    @allure.step("Очистить все wishlists")
    def clear_all_wishlists(self):
        self.browser.get(f"{BASE_URL}/module/blockwishlist/lists")
        while True:
            buttons = self.browser.find_elements(
                "css selector", "a[href*='delete'], .wishlist-delete, button[data-action='delete']"
            )
            if not buttons:
                break
            buttons[0].click()
            try:
                self.browser.switch_to.alert.accept()
            except Exception:
                pass
        return self