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
def created_booking(api_client, auth_token, sample_booking_payload):
    response = api_client.create_booking(sample_booking_payload)
    assert response.status_code == 200, response.text
    booking_id = response.json()["bookingid"]

    yield {
        "id": booking_id,
        "payload": sample_booking_payload,
    }

    api_client.delete_booking(booking_id, auth_token)


@pytest.fixture
def booking_factory(api_client, auth_token, sample_booking_payload):
    """Создаёт брони на основе sample_booking_payload с возможностью переопределить поля."""
    created_ids = []

    def _create(**overrides):
        payload = {**sample_booking_payload, **overrides}
        # bookingdates — вложенный dict, поэтому мержим отдельно
        if "bookingdates" in overrides:
            payload["bookingdates"] = {
                **sample_booking_payload["bookingdates"],
                **overrides["bookingdates"],
            }

        response = api_client.create_booking(payload)
        assert response.status_code == 200, response.text
        booking_id = response.json()["bookingid"]
        created_ids.append(booking_id)
        return {"id": booking_id, "payload": payload}

    yield _create

    for booking_id in created_ids:
        api_client.delete_booking(booking_id, auth_token)