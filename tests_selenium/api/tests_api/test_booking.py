import allure
import pytest


@allure.feature("Booking")
class TestBooking:

    @allure.title("Создание брони с валидным payload")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_booking(self, booking_api, sample_booking_payload):
        response = booking_api.create_booking(sample_booking_payload)

        assert response.status_code == 200, response.text

        data = response.json()
        assert "bookingid" in data, f"Нет bookingid: {data}"
        assert isinstance(data["bookingid"], int), "bookingid должен быть числом"

        # Сервис должен вернуть ровно то, что мы отправили
        assert data["booking"] == sample_booking_payload