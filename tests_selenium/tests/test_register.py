import allure
from faker import Faker

from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.register_page import RegisterPage
from config import BASE_URL


fake = Faker("en_US")


def generate_user_data():
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(
            length=10, special_chars=True, digits=True, upper_case=True
        ),
        "birthdate": fake.date_of_birth(
            minimum_age=18, maximum_age=80
        ).strftime("%m/%d/%Y"),
    }


@allure.epic("Интернет-магазин")
@allure.feature("Регистрация")
class TestRegister:

    @allure.story("Регистрация нового пользователя")
    @allure.title("Проверка регистрации нового пользователя")
    @allure.description(
        "Генерируем данные нового пользователя через Faker, открываем форму "
        "регистрации, заполняем её и проверяем, что после отправки "
        "пользователь автоматически авторизован."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "auth", "register", "smoke")
    def test_register_page(self, browser):
        with allure.step("Генерируем данные нового пользователя"):
            user_data = generate_user_data()
            allure.attach(
                str(user_data),
                name="user_data",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Открываем страницу регистрации"):
            register_page = RegisterPage(browser)
            register_page.open(f"{BASE_URL}/login?create_account=1")

        with allure.step("Заполняем форму регистрации и отправляем"):
            register_page.register(user_data)

        with allure.step("Проверяем, что пользователь авторизован"):
            home_page = HomePage(browser)
            assert home_page.is_user_logged_in(), (
                f"Пользователь {user_data['email']} не залогинен после регистрации"
            )