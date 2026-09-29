import allure
from tests_selenium.api.config_api import API_USERNAME, API_PASSWORD


@allure.epic("Restful Booker API")
@allure.feature("Авторизация")
class TestAuth:

    @allure.story("Создание токена")
    @allure.title("Создание токена с валидными кредами")
    @allure.description(
        "Проверяем, что POST /auth с валидными кредами возвращает 200 "
        "и непустой токен в поле 'token'."
    )
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("api", "auth", "smoke")
    def test_create_token_success(self, api_client):
        with allure.step("Отправляем запрос на создание токена с валидными кредами"):
            response = api_client.create_token(API_USERNAME, API_PASSWORD)

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 200, response.text

        with allure.step("Проверяем наличие и непустоту токена в ответе"):
            body = response.json()
            assert "token" in body, f"Нет токена в ответе: {body}"
            assert body["token"], "Токен пустой"

    @allure.story("Создание токена")
    @allure.title("Создание токена с неверными кредами")
    @allure.description(
        "Проверяем, что POST /auth с неверными кредами возвращает 200, "
        "поле 'reason' присутствует, а 'token' отсутствует."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "auth", "negative")
    def test_create_token_invalid(self, api_client):
        with allure.step("Отправляем запрос на создание токена с неверными кредами"):
            response = api_client.create_token("wrong", "wrong")

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 200, response.text

        with allure.step("Проверяем, что в ответе есть reason и нет token"):
            body = response.json()
            assert "reason" in body, f"Нет поля reason в ответе: {body}"
            assert "token" not in body, "Токен не должен выдаваться при неверных кредах"