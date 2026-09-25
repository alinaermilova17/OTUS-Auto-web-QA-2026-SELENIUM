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