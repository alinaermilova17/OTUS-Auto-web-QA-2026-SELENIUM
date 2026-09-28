import allure


@allure.feature("Фильтрация брони")
class TestBookingFilter:

    @allure.title("Фильтр по checkin/checkout возвращает созданную бронь")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_returns_created_booking(self, api_client, auth_token):
        payload = {
            "firstname": "Filter",
            "lastname": "Test",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-06-10",
                "checkout": "2025-06-20",
            },
            "additionalneeds": "None",
        }

        create_response = api_client.create_booking(payload)
        assert create_response.status_code == 200, create_response.text
        booking_id = create_response.json()["bookingid"]

        try:
            filter_response = api_client.filter_bookings(
                checkin="2025-06-01",
                checkout="2025-06-30",
            )

            assert filter_response.status_code == 200, filter_response.text
            data = filter_response.json()

            assert isinstance(data, list)
            assert len(data) > 0
            for item in data:
                assert "bookingid" in item

            returned_ids = [item["bookingid"] for item in data]
            assert booking_id in returned_ids

            booking_response = api_client.get_booking(booking_id)
            dates = booking_response.json()["bookingdates"]
            assert dates["checkin"] >= "2025-06-01"
            assert dates["checkout"] <= "2025-06-30"

        finally:
            api_client.delete_booking(booking_id, auth_token)

    @allure.title("Фильтр без параметров возвращает все брони")
    def test_filter_no_params_returns_all(self, api_client):
        response = api_client.filter_bookings()

        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    @allure.title("Фильтр с невалидной датой возвращает 400")
    def test_filter_invalid_date_format(self, api_client):
        response = api_client.filter_bookings(
            checkin="not-a-date",
            checkout="2025-06-30",
        )
        assert response.status_code == 500, response.text

    @allure.title("Фильтрация броней по имени")
    def test_filter_by_name(self, api_client):
        response = api_client.get_all_bookings(params={"firstname": "Jim"})
        assert response.status_code == 200