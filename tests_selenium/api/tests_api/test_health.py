import allure


@allure.epic("Restful Booker API")
@allure.feature("Health Check")
class TestHealth:

    @allure.story("Ping")
    @allure.title("GET /ping возвращает 201")
    @allure.description(
        "Проверяем, что health-check эндпоинт GET /ping возвращает 201, "
        "то есть API доступен и работает."
    )
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("api", "health", "smoke")
    def test_ping(self, api_client):
        with allure.step("Отправляем GET /ping"):
            response = api_client.get("/ping")

        with allure.step("Проверяем статус-код 201"):
            assert response.status_code == 201, response.text