import allure


@allure.feature("Booking CRUD")
class TestBookingCrud:

    @allure.title("Создание брони")
    def test_create_booking(self, api_client, sample_booking_payload):
        response = api_client.create_booking(sample_booking_payload)
        assert response.status_code == 200
        data = response.json()
        assert "bookingid" in data
        assert data["booking"]["firstname"] == "Jim"

    @allure.title("Получение брони по ID")
    def test_get_booking(self, api_client, created_booking):
        response = api_client.get_booking(created_booking)
        assert response.status_code == 200
        assert response.json()["lastname"] == "Brown"

    @allure.title("Получение списка всех броней")
    def test_get_all_bookings(self, api_client):
        response = api_client.get_all_bookings()
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @allure.title("Фильтрация броней по имени")
    def test_filter_by_name(self, api_client):
        response = api_client.get_all_bookings(params={"firstname": "Jim"})
        assert response.status_code == 200

    @allure.title("Обновление брони (PUT)")
    def test_update_booking(self, api_client, created_booking, auth_token, sample_booking_payload):
        updated = sample_booking_payload.copy()
        updated["firstname"] = "James"
        response = api_client.update_booking(created_booking, updated, token=auth_token)
        assert response.status_code == 200
        assert response.json()["firstname"] == "James"

    @allure.title("Частичное обновление (PATCH)")
    def test_patch_booking(self, api_client, created_booking, auth_token):
        response = api_client.patch_booking(created_booking, {"firstname": "Jane"}, token=auth_token)
        assert response.status_code == 200
        assert response.json()["firstname"] == "Jane"

    @allure.title("Удаление брони")
    def test_delete_booking(self, api_client, created_booking, auth_token):
        response = api_client.delete_booking(created_booking, token=auth_token)
        assert response.status_code == 201
        # убедимся, что после удаления GET возвращает 404
        get_response = api_client.get_booking(created_booking)
        assert get_response.status_code == 404