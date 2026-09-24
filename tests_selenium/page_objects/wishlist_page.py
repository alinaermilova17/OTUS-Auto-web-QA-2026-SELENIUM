# tests_selenium/page_objects/wishlist_page.py
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tests_selenium.page_objects.base_page import BasePage


class WishlistPage(BasePage):

    # ───── Меню категорий ─────
    CLOTHES_MENU = (By.XPATH, "//li[@id='category-3']//a[contains(@class,'dropdown-item')]")
    WOMEN_LINK   = (By.XPATH, "//ul[contains(@class,'category-sub-menu')]//a[normalize-space()='Women']")

    # ───── Карточка товара ─────
    PRODUCT_BROWN_BEAR = (
        By.CSS_SELECTOR,
        "#js-product-list article.product-miniature a.product-thumbnail"
    )

    # ───── Кнопка wishlist на странице товара ─────
    WISHLIST_BUTTON = (By.CSS_SELECTOR, "button.wishlist-button-add")

    # ───── Модалка wishlist ─────
    WISHLIST_MODAL = (By.CSS_SELECTOR, ".wishlist-modal.modal.fade.show, .wishlist-modal.modal.fade")

    # ← локатор, который вы дали: первый <p> в списке внутри модалки
    WISHLIST_MODAL_ITEM = (
        By.CSS_SELECTOR,
        "#footer .wishlist-modal .modal-body ul li p"
    )

    # ───── Футер ─────
    MY_WISHLIST_FOOTER = (By.CSS_SELECTOR, "#footer_account_list > li:nth-child(5) > a")

    # ───── Страница wishlist ─────
    WISHLIST_LIST_FIRST  = (By.CSS_SELECTOR, "#content > div > ul > li > a > p")
    WISHLIST_PRODUCT_IMG = (
        By.CSS_SELECTOR,
        "#content > ul > li > div > a > div.wishlist-product-image > img"
    )

    # ───────── Actions ─────────

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

    @allure.step("Добавить в wishlist через кнопку + модалку")
    def add_to_wishlist(self):
        # 1. Клик по кнопке wishlist (НЕ по Add to cart!)
        self.click(self.WISHLIST_BUTTON)

        # 2. Ждём модалку выбора списка
        try:
            self.wait_visible(self.WISHLIST_MODAL, timeout=10)

            # 3. Клик по первому списку в модалке
            self.click(self.WISHLIST_MODAL_ITEM)

            # 4. Ждём, что модалка закрылась
            self.wait.until(
                EC.invisibility_of_element_located(self.WISHLIST_MODAL)
            )
        except TimeoutException:
            # модалки нет — товар уже был в wishlist, ничего не делаем
            allure.attach(
                self.browser.get_screenshot_as_png(),
                "modal_not_found",
                allure.attachment_type.PNG
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

    # ───────── Helpers ─────────

    def _close_modal_if_present(self):
        try:
            modal = self.browser.find_element(*self.WISHLIST_MODAL)
            if modal.is_displayed():
                close_btn = modal.find_element(
                    By.CSS_SELECTOR, "button.close, [data-dismiss='modal']"
                )
                self.browser.execute_script("arguments[0].click();", close_btn)
                self.wait.until(
                    EC.invisibility_of_element_located(self.WISHLIST_MODAL)
                )
        except Exception:
            pass