import allure

from tests_selenium.page_objects.login_page import LoginPage
from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.wishlist_page import WishlistPage
from config import LOGIN, PASSWORD, BASE_URL


@allure.epic("UI")
@allure.feature("Wishlist")
class TestWishlist:

    # ─────────── helper ───────────

    def _login(self, browser):
        """Общий шаг: логин через LoginPage, проверка через HomePage."""
        LoginPage(browser).open(f"{BASE_URL}/login?back=my-account") \
                          .login(LOGIN, PASSWORD)
        assert HomePage(browser).is_user_logged_in(), "Пользователь не залогинен"

    # ─────────── tests ───────────

    @allure.title("Добавить товар 'Brown bear printed sweater' в wishlist")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Добавление")
    def test_add_product_to_wishlist(self, browser):
        with allure.step("Залогиниться"):
            self._login(browser)

        page = WishlistPage(browser)

        with allure.step("Открыть Clothes → Women"):
            page.open_women_category()

        with allure.step("Открыть карточку 'Brown bear printed sweater'"):
            page.open_brown_bear_product()
            assert page.is_product_opened("Brown bear printed sweater"), \
                "Открылась не та карточка товара"

        with allure.step("Добавить товар в wishlist"):
            page.add_to_wishlist()

        with allure.step("Проверить, что появился тост 'Product added'"):
            page.wait_for_added_toast()

    @allure.title("Проверить, что товар сохранён в My wishlist")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Просмотр")
    def test_product_present_in_wishlist(self, browser):
        with allure.step("Залогиниться"):
            self._login(browser)

        page = WishlistPage(browser)

        with allure.step("Добавить товар в wishlist"):
            page.open_women_category() \
                .open_brown_bear_product() \
                .add_to_wishlist()
            page.wait_for_added_toast()

        with allure.step("Открыть 'My wishlist'"):
            page.open_my_wishlist()

        with allure.step("Проверить, что товар есть в списке"):
            assert page.has_product("Brown bear printed sweater"), \
                "Товар не найден в wishlist"

    @allure.title("Toggle wishlist: добавить и убрать товар")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Toggle")
    def test_toggle_wishlist(self, browser):
        with allure.step("Залогиниться"):
            self._login(browser)

        page = WishlistPage(browser)

        with allure.step("Открыть карточку товара"):
            page.open_women_category().open_brown_bear_product()

        with allure.step("Добавить в wishlist (favorite_border → favorite)"):
            page.add_to_wishlist()
            page.wait_for_added_toast()

        with allure.step("Убрать из wishlist (favorite → favorite_border)"):
            page.toggle_wishlist()

        with allure.step("Проверить, что иконка вернулась в 'favorite_border'"):
            assert page.is_wishlist_icon_border(), \
                "Иконка не вернулась в исходное состояние"