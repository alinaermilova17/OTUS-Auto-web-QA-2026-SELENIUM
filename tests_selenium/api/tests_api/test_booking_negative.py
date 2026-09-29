import allure


@allure.epic("Restful Booker API")
@allure.feature("Booking Negative")
class TestBookingNegative:

    @allure.story("Read")
    @allure.title("GET несуществующей брони")
    @allure.description(
        "Проверяем, что GET /booking/{id} для несуществующего ID "
        "возвращает 404."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "booking", "negative", "read")
    def test_get_nonexistent_booking(self, api_client):
        with allure.step("Запрашиваем бронь с несуществующим ID"):
            response = api_client.get_booking(999999999)

        with allure.step("Проверяем статус-код 404"):
            assert response.status_code == 404, response.text

    @allure.story("Update")
    @allure.title("PUT без авторизации")
    @allure.description(
        "Проверяем, что PUT /booking/{id} без токена авторизации "
        "возвращает 403."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "booking", "negative", "auth", "update")
    def test_update_without_auth(self, api_client, created_booking, sample_booking_payload):
        with allure.step("Отправляем PUT без токена"):
            response = api_client.update_booking(
                created_booking["id"], sample_booking_payload, token=None
            )

        with allure.step("Проверяем статус-код 403"):
            assert response.status_code == 403, response.text

    @allure.story("Delete")
    @allure.title("DELETE без авторизации")
    @allure.description(
        "Проверяем, что DELETE /booking/{id} без токена авторизации "
        "возвращает 403."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "booking", "negative", "auth", "delete")
    def test_delete_without_auth(self, api_client, created_booking):
        with allure.step("Отправляем DELETE без токена"):
            response = api_client.delete_booking(created_booking["id"], token=None)

        with allure.step("Проверяем статус-код 403"):
            assert response.status_code == 403, response.text

    @allure.story("Create")
    @allure.title("Создание брони с пустым телом")
    @allure.description(
        "Проверяем, что POST /booking с пустым телом {} "
        "возвращает 500."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "booking", "negative", "create")
    def test_create_empty_payload(self, api_client):
        with allure.step("Отправляем POST с пустым телом"):
            response = api_client.create_booking({})

        with allure.step("Проверяем статус-код 500"):
            assert response.status_code == 500, response.text

    @allure.story("Delete")
    @allure.title("Повторное удаление уже удалённой брони возвращает 404")
    @allure.description(
        "Создаём бронь, удаляем её, затем пытаемся удалить повторно — "
        "ожидаем 404/405. Через GET убеждаемся, что брони действительно нет."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "booking", "negative", "delete")
    def test_delete_already_deleted_booking(
            self,
            api_client,
            sample_booking_payload,
            auth_token,
    ):
        with allure.step("Создаём бронь"):
            create_response = api_client.create_booking(sample_booking_payload)
            assert create_response.status_code == 200, create_response.text
            booking_id = create_response.json()["bookingid"]

        with allure.step("Удаляем бронь первый раз — ожидаем 201"):
            first_delete = api_client.delete_booking(booking_id, auth_token)
            assert first_delete.status_code == 201, first_delete.text

        with allure.step("Пытаемся удалить повторно — ожидаем 404/405"):
            second_delete = api_client.delete_booking(booking_id, auth_token)
            assert second_delete.status_code in (404, 405), (
                f"Ожидали 404/405, получили {second_delete.status_code}: "
                f"{second_delete.text}"
            )

        with allure.step("Проверяем через GET, что брони действительно нет"):
            get_response = api_client.get(f"/booking/{booking_id}")
            assert get_response.status_code == 404, get_response.text

    @allure.story("Update")
    @allure.title("PUT без обязательного поля firstname")
    @allure.description(
        "Проверяем, что PUT /booking/{id} без поля firstname "
        "возвращает 400."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "booking", "negative", "validation", "update")
    def test_update_booking_without_firstname(
            self,
            api_client,
            created_booking,
            auth_token,
            sample_booking_payload,
    ):
        updated = sample_booking_payload.copy()
        updated.pop("firstname")

        with allure.step("Отправляем PUT без поля firstname"):
            response = api_client.update_booking(
                created_booking, updated, token=auth_token,
            )

        with allure.step("Проверяем статус-код 400"):
            assert response.status_code == 400, response.text