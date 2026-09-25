import allure


@allure.epic("API")
@allure.feature("Health Check")
class TestHealth:

    @allure.title("GET /ping возвращает 201")
    def test_ping(self, api_client):
        response = api_client.get("/ping")
        assert response.status_code == 201