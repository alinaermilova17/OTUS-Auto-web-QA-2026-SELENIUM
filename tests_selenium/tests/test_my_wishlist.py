# tests_selenium/tests/test_my_wishlist.py
import allure
import pytest

from tests_selenium.page_objects.login_page import LoginPage
from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.wishlist_page import WishlistPage
from config import LOGIN, PASSWORD, BASE_URL


@allure.epic("UI")
@allure.feature("Wishlist")
class TestWishlist:

    def _login(self, browser):
        login_page = LoginPage(browser)
        login_page.open(f"{BASE_URL}/login?back=my-account")
        login_page.login(LOGIN, PASSWORD)
        assert HomePage(browser).is_user_logged_in(), "Пользователь не залогинен"

    @allure.title("Добавить товар в wishlist")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Добавление")
    def test_add_product_to_wishlist(self, browser):
        with allure.step("Залогиниться"):
            self._login(browser)

        page = WishlistPage(browser)

        with allure.step("Открыть Clothes → Women"):
            page.open_women_category()

        with allure.step("Открыть карточку товара"):
            page.open_brown_bear_product()
            assert page.is_product_opened(), \
                f"Открылась не та карточка: {browser.current_url}"

        with allure.step("Добавить в wishlist через модалку"):
            page.add_to_wishlist()

    @allure.title("Проверить, что товар сохранён в My wishlist")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Просмотр")
    def test_product_present_in_wishlist(self, browser):
        with allure.step("Залогиниться"):
            self._login(browser)

        page = WishlistPage(browser)

        with allure.step("Открыть Clothes → Women"):
            page.open_women_category()

        with allure.step("Открыть карточку товара"):
            page.open_brown_bear_product()

        with allure.step("Добавить в wishlist через модалку"):
            page.add_to_wishlist()

        with allure.step("Перейти в My wishlists через футер"):
            page.open_my_wishlist()

        with allure.step("Открыть первый сохранённый wishlist"):
            page.open_first_wishlist()

        with allure.step("Проверить, что товар есть в wishlist"):
            assert page.has_product_in_wishlist(), \
                "Товар не найден в wishlist"