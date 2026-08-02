from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.login_page import LoginPage
from tests_selenium.page_objects.cart_page import CartPage
from config import LOGIN, PASSWORD, BASE_URL


def test_add_to_cart(browser):
    login_page = LoginPage(browser)
    home_page = HomePage(browser)

    login_page.open(f'{BASE_URL}/login')
    login_page.login(LOGIN, PASSWORD)

    assert home_page.is_user_logged_in()
    cart_page = CartPage(browser)
    cart_page.add_to_cart()
    cart_page.open_cart()

    cart_count = cart_page.get_current_quantity()
    assert cart_count > 0, f'В корзине {cart_count} товаров, ожидался минимум 1'

    print(f'Товар успешно добавлен в корзину! Количество: {cart_count}')

