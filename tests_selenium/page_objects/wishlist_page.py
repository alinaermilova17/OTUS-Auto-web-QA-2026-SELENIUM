import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage


class WishlistPage(BasePage):
    CLOTHES_MENU = (By.XPATH, "//li[@id='category-3']//a[contains(@class,'dropdown-item')]")
    WOMEN_LINK  = (By.XPATH, "//ul[contains(@class,'category-sub-menu')]//a[normalize-space()='Women']")
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
    WISHLIST_ITEM_ROW        = (By.CSS_SELECTOR, "#content > ul > li")
    DELETE_ITEM_BUTTON       = (By.CSS_SELECTOR, "#content > ul > li > div > div > button.wishlist-button-add")
    DELETE_MODAL             = (By.CSS_SELECTOR, ".wishlist-delete .wishlist-modal.modal.fade.show")
    DELETE_MODAL_CONFIRM_BTN = (
        By.CSS_SELECTOR,
        ".wishlist-delete .wishlist-modal.modal.fade.show "
        ".modal-footer > button.btn.btn-primary"
    )


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

    @allure.step("Добавить в wishlist (если ещё не добавлен)")
    def ensure_in_wishlist(self):
        icon = self.find(self.WISHLIST_ICON)
        classes = icon.get_attribute("class") or ""
        allure.attach(classes, "icon class before", allure.attachment_type.TEXT)

        if "favorite_border" in classes:
            self.click(self.WISHLIST_BUTTON)
            self.wait.until(
                lambda d: "favorite_border" not in (
                        d.find_element(*self.WISHLIST_ICON).get_attribute("class") or ""
                )
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

    @allure.step("Очистить первый wishlist от всех товаров")
    def clear_all_wishlists(self):
        """
        Открывает My wishlists → первый список → удаляет все товары.
        """
        # 1. Перейти в футер → My wishlists
        self.open_my_wishlist()

        # 2. Открыть первый список
        self.open_first_wishlist()

        # 3. Пока есть товары — удалять их
        max_iterations = 20  # защита от бесконечного цикла
        iteration = 0
        while iteration < max_iterations:
            iteration += 1

            # есть ли хотя бы один товар в списке
            items = self.browser.find_elements(*self.WISHLIST_ITEM_ROW)
            if not items:
                allure.attach(
                    f"wishlist пуст (итерация {iteration})",
                    "clear wishlist",
                    allure.attachment_type.TEXT
                )
                break

            allure.attach(
                f"удаляем товар #{iteration}",
                "clear wishlist",
                allure.attachment_type.TEXT
            )

            # 4. клик по кнопке удаления первого товара
            delete_btn = self.wait_clickable(self.DELETE_ITEM_BUTTON)
            self.browser.execute_script("arguments[0].click();", delete_btn)

            # 5. ждём модалку подтверждения
            self.wait_visible(self.DELETE_MODAL, timeout=10)

            # 6. клик по кнопке подтверждения в модалке
            confirm_btn = self.wait_clickable(self.DELETE_MODAL_CONFIRM_BTN)
            self.browser.execute_script("arguments[0].click();", confirm_btn)

            # 7. ждём, что модалка исчезла
            self.wait_invisible(self.DELETE_MODAL)

            # 8. ждём, что список обновился (товар исчез)
            try:
                self.wait.until(
                    lambda d: len(d.find_elements(*self.WISHLIST_ITEM_ROW)) < len(items)
                )
            except TimeoutException:
                allure.attach(
                    self.browser.get_screenshot_as_png(),
                    f"item_not_removed_{iteration}",
                    allure.attachment_type.PNG
                )

        return self