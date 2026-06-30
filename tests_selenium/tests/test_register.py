from faker import Faker
from tests_selenium.page_objects.home_page import HomePage
from tests_selenium.page_objects.register_page import RegisterPage
from config import BASE_URL

fake = Faker('en_US')


def generate_user_data():
    return {
        'firstname': fake.first_name(),
        'lastname': fake.last_name(),
        'email': fake.email(),
        'password': fake.password(length=10, special_chars=True, digits=True, upper_case=True),
        'birthdate': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%m/%d/%Y')
    }


def test_register_page(browser):
    user_data = generate_user_data()
    register_page = RegisterPage(browser)
    register_page.open(f'{BASE_URL}/registration')
    register_page.register(user_data)
    home_page = HomePage(browser)

    assert home_page.is_user_logged_in(), (
f"Пользователь {user_data['email']} не залогинен после регистрации")
