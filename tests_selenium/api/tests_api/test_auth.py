import allure
from tests_selenium.api.config_api import API_USERNAME, API_PASSWORD

@allure.feature("Авторизация")
class TestAuth:

    @allure.title("Создание токена с валидными кредами")
    def test_create_token_success(self, api_client):
        response = api_client.create_token(API_USERNAME, API_PASSWORD)
        assert response.status_code == 200, response.text
        body = response.json()
        assert "token" in body, f"Нет токена в ответе: {body}"
        assert body["token"], "Токен пустой"

    @allure.title("Создание токена с неверными кредами")
    def test_create_token_invalid(self, api_client):
        response = api_client.create_token("wrong", "wrong")
        assert response.status_code == 200, response.text
        body = response.json()
        assert "reason" in body, f"Нет поля reason в ответе: {body}"
        assert "token" not in body, "Токен не должен выдаваться при неверных кредах"