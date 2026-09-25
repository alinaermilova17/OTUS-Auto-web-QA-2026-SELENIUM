import allure


@allure.feature("Auth")
class TestAuth:

    @allure.title("Создание токена с валидными кредами")
    def test_create_token_success(self, api_client):
        response = api_client.create_token("admin", "password123")
        assert response.status_code == 200
        assert "token" in response.json()

    @allure.title("Создание токена с неверными кредами")
    def test_create_token_invalid(self, api_client):
        response = api_client.create_token("wrong", "wrong")
        assert response.status_code == 200
        assert "reason" in response.json()