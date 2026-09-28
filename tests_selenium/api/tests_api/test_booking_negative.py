import allure


@allure.feature("Booking Negative")
class TestBookingNegative:

    @allure.title("GET несуществующей брони")
    def test_get_nonexistent_booking(self, api_client):
        response = api_client.get_booking(999999999)
        assert response.status_code == 404

    @allure.title("PUT без авторизации")
    def test_update_without_auth(self, api_client, created_booking, sample_booking_payload):
        response = api_client.update_booking(created_booking, sample_booking_payload, token=None)
        assert response.status_code == 403

    @allure.title("DELETE без авторизации")
    def test_delete_without_auth(self, api_client, created_booking):
        response = api_client.delete_booking(created_booking, token=None)
        assert response.status_code == 403

    @allure.title("Создание брони с пустым телом")
    def test_create_empty_payload(self, api_client):
        response = api_client.create_booking({})
        assert response.status_code == 500

    @allure.title("Повторное удаление уже удалённой брони возвращает 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_already_deleted_booking(
            self,
            api_client,
            sample_booking_payload,
            auth_token,
    ):
        # 1. Создаём бронь
        create_response = api_client.create_booking(sample_booking_payload)
        assert create_response.status_code == 200, create_response.text
        booking_id = create_response.json()["bookingid"]

        # 2. Удаляем её первый раз — успех
        first_delete = api_client.delete_booking(booking_id, auth_token)
        assert first_delete.status_code == 201, first_delete.text

        # 3. Пытаемся удалить повторно — брони уже нет
        second_delete = api_client.delete_booking(booking_id, auth_token)

        assert second_delete.status_code in (404, 405), (
            f"Ожидали 404/405, получили {second_delete.status_code}: "
            f"{second_delete.text}"
        )

        # 4. Проверяем через GET, что брони действительно нет
        get_response = api_client.get(f"/booking/{booking_id}")
        assert get_response.status_code == 404, get_response.text