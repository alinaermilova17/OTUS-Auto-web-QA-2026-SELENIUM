import allure
import pytest


@allure.epic("Restful Booker API")
@allure.feature("Booking CRUD")
class TestBookingCrud:

    @allure.story("Create")
    @allure.title("Создание брони")
    @allure.description(
        "Проверяем, что POST /booking создаёт бронь и возвращает bookingid, "
        "а поля сохранённой брони совпадают с переданными."
    )
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("api", "booking", "crud", "create", "smoke")
    def test_create_booking(self, api_client, sample_booking_payload):
        with allure.step("Отправляем запрос на создание брони"):
            response = api_client.create_booking(sample_booking_payload)

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 200, response.text

        with allure.step("Проверяем наличие bookingid и корректность полей"):
            data = response.json()
            assert "bookingid" in data, f"Нет bookingid в ответе: {data}"
            assert data["booking"]["firstname"] == "Jim"

    @allure.story("Read")
    @allure.title("Получение брони по ID")
    @allure.description(
        "Проверяем, что GET /booking/{id} возвращает 200 и корректные данные "
        "ранее созданной брони."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "booking", "crud", "read", "smoke")
    def test_get_booking(self, api_client, created_booking):
        with allure.step("Запрашиваем бронь по ID"):
            response = api_client.get_booking(created_booking["id"])

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 200, response.text

        with allure.step("Проверяем поле lastname"):
            assert response.json()["lastname"] == "Brown"

    @allure.story("Read")
    @allure.title("Получение списка всех броней")
    @allure.description(
        "Проверяем, что GET /booking возвращает 200 и список броней."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "booking", "crud", "read")
    def test_get_all_bookings(self, api_client):
        with allure.step("Запрашиваем список всех броней"):
            response = api_client.get_all_bookings()

        with allure.step("Проверяем статус-код и тип данных"):
            assert response.status_code == 200, response.text
            assert isinstance(response.json(), list), (
                f"Ожидался list, получено: {type(response.json())}"
            )

    @allure.story("Update")
    @allure.title("Обновление поля '{field}' через PUT")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "booking", "crud", "update")
    @pytest.mark.parametrize(
        "field, new_value",
        [
            ("firstname", "James"),
            ("lastname", "Smith"),
            ("totalprice", 999),
            ("depositpaid", False),
            ("additionalneeds", "Dinner"),
            (
                    "bookingdates",
                    {"checkin": "2025-07-01", "checkout": "2025-07-10"},
            ),
        ],
        ids=[
            "firstname",
            "lastname",
            "totalprice",
            "depositpaid",
            "additionalneeds",
            "bookingdates",
        ],
    )
    def test_update_booking(
            self,api_client,created_booking,auth_token,sample_booking_payload,field,new_value,
    ):
        updated = sample_booking_payload.copy()
        updated[field] = new_value

        with allure.step(f"Отправляем PUT с {field}={new_value!r}"):
            response = api_client.update_booking(
                created_booking["id"], updated, token=auth_token,
            )

        with allure.step("Проверяем статус-код и обновлённое поле"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert data[field] == new_value, (
                f"Поле '{field}' не обновилось: "
                f"ожидали {new_value!r}, получили {data[field]!r}"
            )

            for key, value in sample_booking_payload.items():
                if key == field:
                    continue
                assert data[key] == value, (
                    f"Поле '{key}' не должно было меняться: "
                    f"ожидали {value!r}, получили {data[key]!r}"
                )

        with allure.step("Проверяем через GET, что изменение сохранилось"):
            get_response = api_client.get_booking(created_booking["id"])
            assert get_response.status_code == 200, get_response.text
            assert get_response.json()[field] == new_value

    @allure.story("Update")
    @allure.title("Частичное обновление (PATCH)")
    @allure.description(
        "Проверяем, что PATCH /booking/{id} частично обновляет бронь. "
        "Меняем только firstname на 'Jane' и проверяем результат."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "booking", "crud", "patch")
    def test_patch_booking(self, api_client, created_booking, auth_token):
        with allure.step("Отправляем PATCH-запрос с новым firstname"):
            response = api_client.patch_booking(
                created_booking["id"], {"firstname": "Jane"}, token=auth_token
            )

        with allure.step("Проверяем статус-код и обновлённое поле"):
            assert response.status_code == 200, response.text
            assert response.json()["firstname"] == "Jane"

    @allure.story("Delete")
    @allure.title("Удаление брони")
    @allure.description(
        "Проверяем, что DELETE /booking/{id} удаляет бронь (201), "
        "а последующий GET возвращает 404."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "booking", "crud", "delete")
    def test_delete_booking(self, api_client, created_booking, auth_token):
        with allure.step("Отправляем DELETE-запрос"):
            response = api_client.delete_booking(created_booking["id"], token=auth_token)

        with allure.step("Проверяем статус-код удаления (201)"):
            assert response.status_code == 201, response.text

        with allure.step("Проверяем, что бронь больше недоступна (GET -> 404)"):
            get_response = api_client.get_booking(created_booking)
            assert get_response.status_code == 404, (
                f"Ожидался 404, получен {get_response.status_code}: {get_response.text}"
            )


