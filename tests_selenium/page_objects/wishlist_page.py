import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tests_selenium.page_objects.base_page import BasePage


class WishlistPage(BasePage):

    # Меню
    CLOTHES_MENU = (By.XPATH, "//li[@id='category-3']//a[contains(@class,'dropdown-item')]")
    WOMEN_LINK   = (By.XPATH, "//ul[contains(@class,'category-sub-menu')]//a[normalize-space()='Women']")

    # Карточка конкретного товара
    PRODUCT_BROWN_BEAR = (
        By.CSS_SELECTOR,
        "a[href*='brown-bear-printed-sweater']"
    )

    # Кнопка wishlist на странице товара
    WISHLIST_BUTTON = (By.CSS_SELECTOR, "button.wishlist-button-add")

    # Модалка + пункт внутри
    WISHLIST_MODAL = (By.CSS_SELECTOR, ".wishlist-modal.modal.show, .wishlist-modal.modal.fade.show")
    WISHLIST_MODAL_ITEM = (
        By.CSS_SELECTOR,
        ".wishlist-modal.modal.show .modal-body ul li p, "
        ".wishlist-modal.modal.fade.show .modal-body ul li p"
    )

    # Футер и страница wishlist
    MY_WISHLIST_FOOTER   = (By.CSS_SELECTOR, "#footer_account_list > li:nth-child(5) > a")
    WISHLIST_LIST_FIRST  = (By.CSS_SELECTOR, "#content > div > ul > li > a > p")
    WISHLIST_PRODUCT_IMG = (By.CSS_SELECTOR, "#content > ul > li > div > a > div.wishlist-product-image > img")

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

    @allure.step("Добавить в wishlist")
    def add_to_wishlist(self):
        # 1. клик по кнопке wishlist
        self.click(self.WISHLIST_BUTTON)

        # 2. ждём PRESENCE (а не visibility) — модалка появляется с анимацией
        try:
            self.wait.until(EC.presence_of_element_located(self.WISHLIST_MODAL))
            # 3. ждём кликабельности пункта внутри модалки
            item = self.wait.until(EC.element_to_be_clickable(self.WISHLIST_MODAL_ITEM))
            self.browser.execute_script("arguments[0].click();", item)
            # 4. ждём закрытия
            self.wait.until(EC.invisibility_of_element_located(self.WISHLIST_MODAL))
        except TimeoutException:
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