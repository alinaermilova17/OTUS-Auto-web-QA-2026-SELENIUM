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

    # ───── Карточка товара в каталоге ─────
    PRODUCT_BROWN_BEAR = (
        By.CSS_SELECTOR,
        "#js-product-list article.product-miniature a.product-thumbnail"
    )

    # ───── Страница товара ─────
    PRODUCT_TITLE   = (By.CSS_SELECTOR, "h1.h1, h1[itemprop='name']")
    ADD_TO_CART     = (
        By.CSS_SELECTOR,
        "#add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > button"
    )

    # ───── Модалка выбора wishlist ─────
    WISHLIST_MODAL       = (By.CSS_SELECTOR, ".wishlist-modal.modal.show")
    WISHLIST_MODAL_ITEM  = (
        By.CSS_SELECTOR,
        ".wishlist-modal.modal.show .modal-body ul li"
    )
    WISHLIST_MODAL_CLOSE = (By.CSS_SELECTOR, ".wishlist-modal.modal.show button.close")

    # ───── Футер ─────
    MY_WISHLIST_FOOTER = (By.CSS_SELECTOR, "#footer_account_list > li:nth-child(5) > a")

    # ───── Страница wishlist ─────
    WISHLIST_LIST_FIRST = (By.CSS_SELECTOR, "#content > div > ul > li > a > p")
    WISHLIST_PRODUCT_IMG = (
        By.CSS_SELECTOR,
        "#content > ul > li > div > a > div.wishlist-product-image > img"
    )

    # ───────── Actions ─────────

    @allure.step("Открыть категорию Clothes → Women")
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

    @allure.step("Добавить товар в wishlist (через кнопку 'Add to cart area' и модалку)")
    def add_to_wishlist(self):
        # 1. клик по кнопке wishlist в блоке add-to-cart
        self.click(self.ADD_TO_CART)

        # 2. дождаться модалки
        self.wait_visible(self.WISHLIST_MODAL, timeout=15)

        # 3. выбрать первый wishlist в списке
        self.click(self.WISHLIST_MODAL_ITEM)

        return self

    @allure.step("Скролл вниз")
    def scroll_down(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self

    @allure.step("Перейти в 'My wishlists' через футер")
    def open_my_wishlist(self):
        # закрываем модалку, если она ещё открыта
        self._close_modal_if_present()
        # скроллим вниз, чтобы футер был виден
        self.scroll_down()
        # клик по ссылке в футере
        self.click(self.MY_WISHLIST_FOOTER)
        return self

    @allure.step("Открыть первый сохранённый wishlist")
    def open_first_wishlist(self):
        self.click(self.WISHLIST_LIST_FIRST)
        return self

    # ───────── Checks ─────────

    @allure.step("Проверить, что товар есть в wishlist")
    def has_product_in_wishlist(self) -> bool:
        return self.is_visible(self.WISHLIST_PRODUCT_IMG)

    # ───────── Helpers ─────────

    def _close_modal_if_present(self):
        try:
            modal = self.browser.find_element(*self.WISHLIST_MODAL)
            if modal.is_displayed():
                close_btn = modal.find_element(*self.WISHLIST_MODAL_CLOSE)
                self.browser.execute_script("arguments[0].click();", close_btn)
                self.wait.until(EC.invisibility_of_element_located(self.WISHLIST_MODAL))
        except Exception:
            pass