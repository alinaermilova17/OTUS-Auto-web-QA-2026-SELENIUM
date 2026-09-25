import allure
from tests_selenium.page_objects.login_page import LoginPage
from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.catalog_page import CatalogPage
from config import LOGIN, PASSWORD, BASE_URL


class TestCatalogSort:

    def _login(self, browser):
        login_page = LoginPage(browser)
        login_page.open(f"{BASE_URL}/login?back=my-account")
        login_page.login(LOGIN, PASSWORD)
        assert HomePage(browser).is_user_logged_in(), "Пользователь не залогинен"


    @allure.title("Сортировка Art по названию (Z → A)")
    def test_sort_by_name_desc(self, browser):
        with allure.step("Залогиниться"):
            self._login(browser)

        page = CatalogPage(browser)

        with allure.step("Открыть категорию Art"):
            page.open_art_by_url()

        with allure.step("Сортировать по названию (Z → A)"):
            page.sort_by("price", "desc")

        with allure.step("Проверить, что названия идут по убыванию"):
            names = page.get_names()
            assert names, "Не найдено ни одного названия на странице"
            assert names == sorted(names, key=str.lower, reverse=True), \
                f"Названия не отсортированы Z → A: {names}"