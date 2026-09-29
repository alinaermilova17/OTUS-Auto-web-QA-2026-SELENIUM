import allure

from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.login_page import LoginPage
from tests_selenium.page_objects.cart_page import CartPage
from config import LOGIN, PASSWORD, BASE_URL


@allure.epic("Интернет-магазин")
@allure.feature("Корзина")
class TestCart:

    @allure.story("Удаление товара")
    @allure.title("Проверка удаления товара из корзины")
    @allure.description(
        "Авторизуемся, добавляем товар в корзину, затем удаляем его и "
        "проверяем, что корзина пуста (по subtotal)."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "cart", "smoke")
    def test_delete_from_cart(self, browser):
        with allure.step("Авторизуемся в системе"):
            login_page = LoginPage(browser)
            login_page.open(f"{BASE_URL}/login")
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Проверяем, что пользователь авторизован"):
            home_page = HomePage(browser)
            assert home_page.is_user_logged_in(), "Пользователь не авторизован"

        with allure.step("Добавляем товар в корзину"):
            cart_page = CartPage(browser)
            cart_page.add_to_cart()

        with allure.step("Закрываем модальное окно и открываем корзину"):
            cart_page.close_cart_modal()
            cart_page.open_cart()

        with allure.step("Проверяем, что в корзине есть хотя бы один товар"):
            cart_count = cart_page.get_current_quantity()
            assert cart_count > 0, (
                f"В корзине {cart_count} товаров, ожидался минимум 1")

        with allure.step("Удаляем товар из корзины"):
            cart_page.delete_from_cart()

        with allure.step("Проверяем, что корзина пуста"):
           cart_page.is_cart_empty_by_subtotal()


