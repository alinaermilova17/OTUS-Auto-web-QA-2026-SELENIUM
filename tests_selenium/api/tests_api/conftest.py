import pytest
from tests_selenium.api.api_clients.booking_api import BookingApi


@pytest.fixture(scope="session")
def api_client():
    return BookingApi()


@pytest.fixture(scope="session")
def auth_token(api_client):
    response = api_client.create_token()
    assert response.status_code == 200
    token = response.json().get("token")
    assert token, "Не удалось получить токен"
    return token


@pytest.fixture
def sample_booking_payload():
    return {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-01-01",
            "checkout": "2026-01-05"
        },
        "additionalneeds": "Breakfast"
    }


@pytest.fixture
def created_booking(api_client, sample_booking_payload):
    response = api_client.create_booking(sample_booking_payload)
    assert response.status_code == 200
    booking_id = response.json()["bookingid"]
    yield booking_id
    try:
        api_client.delete_booking(booking_id, token=auth_token)
    except Exception:
        pass