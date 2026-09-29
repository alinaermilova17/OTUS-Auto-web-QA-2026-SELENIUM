import allure


@allure.epic("Restful Booker API")
@allure.feature("Фильтрация брони")
class TestBookingFilter:

    @allure.story("Фильтр по датам")
    @allure.title("Фильтр по checkin/checkout возвращает созданную бронь")
    @allure.description(
        "Создаём бронь через фикстуру created_booking, затем запрашиваем "
        "фильтр по широкому диапазону дат и проверяем, что созданная бронь "
        "присутствует в выдаче, а её даты совпадают с ожидаемыми."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "booking", "filter", "dates")
    def test_filter_returns_created_booking(self, api_client, created_booking):
        booking_id = created_booking["id"]
        allure.attach(
            str(booking_id),
            name="booking_id",
            attachment_type=allure.attachment_type.TEXT,
        )

        with allure.step("Запрашиваем фильтр по широкому диапазону дат"):
            filter_response = api_client.filter_bookings(
                checkin="2025-12-01",
                checkout="2026-12-31",
            )

        with allure.step("Проверяем статус-код и структуру ответа"):
            assert filter_response.status_code == 200, filter_response.text
            data = filter_response.json()
            assert isinstance(data, list), f"Ожидался list, получено: {type(data)}"
            assert len(data) > 0, f"Фильтр вернул пустой список: {data}"
            assert all("bookingid" in item for item in data), (
                f"Не у всех элементов есть bookingid: {data}"
            )

        with allure.step("Проверяем, что созданная бронь есть в выдаче"):
            returned_ids = [item["bookingid"] for item in data]
            assert booking_id in returned_ids, (
                f"Бронь {booking_id} не найдена. Полученные id: {returned_ids}"
            )

        with allure.step("Проверяем, что даты брони совпадают с ожидаемыми"):
            booking_response = api_client.get_booking(booking_id)
            dates = booking_response.json()["bookingdates"]
            assert dates["checkin"] == "2026-01-01"
            assert dates["checkout"] == "2026-01-05"

    @allure.story("Фильтр без параметров")
    @allure.title("Фильтр без параметров возвращает все брони")
    @allure.description(
        "Проверяем, что вызов фильтра без параметров возвращает 200 "
        "и непустой список броней."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "booking", "filter", "smoke")
    def test_filter_no_params_returns_all(self, api_client):
        with allure.step("Запрашиваем фильтр без параметров"):
            response = api_client.filter_bookings()

        with allure.step("Проверяем статус-код и структуру ответа"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert isinstance(data, list), f"Ожидался list, получено: {type(data)}"
            assert len(data) > 0, f"Ожидался непустой список, получено: {data}"

    @allure.story("Невалидные параметры")
    @allure.title("Фильтр с невалидной датой возвращает 500")
    @allure.description(
        "Проверяем, что фильтр с невалидным форматом даты (не YYYY-MM-DD) "
        "возвращает 500."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "booking", "filter", "negative", "validation")
    def test_filter_invalid_date_format(self, api_client):
        with allure.step("Отправляем фильтр с невалидной датой checkin"):
            response = api_client.filter_bookings(
                checkin="not-a-date",
                checkout="2026-01-05",
            )

        with allure.step("Проверяем статус-код 500"):
            assert response.status_code == 500, response.text

    @allure.story("Фильтр по имени")
    @allure.title("Фильтрация броней по имени")
    @allure.description(
        "Создаём бронь с firstname='Jim' через booking_factory и проверяем, "
        "что фильтр по firstname возвращает эту бронь."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "booking", "filter", "firstname")
    def test_filter_by_name(self, api_client, booking_factory):
        with allure.step("Создаём бронь с firstname='Jim'"):
            booking = booking_factory(firstname="Jim")
            allure.attach(
                str(booking["id"]),
                name="booking_id",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Запрашиваем фильтр по firstname='Jim'"):
            response = api_client.get_all_bookings(params={"firstname": "Jim"})

        with allure.step("Проверяем статус-код и наличие брони в выдаче"):
            assert response.status_code == 200, response.text
            returned_ids = [item["bookingid"] for item in response.json()]
            assert booking["id"] in returned_ids, (
                f"Бронь {booking['id']} не найдена. Полученные id: {returned_ids}"
            )

    @allure.story("Фильтр по фамилии")
    @allure.title("Фильтрация броней по фамилии")
    @allure.description(
        "Создаём бронь с lastname='Brown' через booking_factory и проверяем, "
        "что фильтр по lastname возвращает эту бронь, а у всех найденных "
        "броней фамилия действительно 'Brown'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "booking", "filter", "lastname")
    def test_filter_by_lastname(self, api_client, booking_factory):
        with allure.step("Создаём бронь с lastname='Brown'"):
            booking = booking_factory(lastname="Brown")
            allure.attach(
                str(booking["id"]),
                name="booking_id",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Запрашиваем фильтр по lastname='Brown'"):
            response = api_client.get_all_bookings(params={"lastname": "Brown"})

        with allure.step("Проверяем статус-код и структуру ответа"):
            assert response.status_code == 200, response.text
            data = response.json()
            assert isinstance(data, list), f"Ожидался list, получено: {type(data)}"
            assert len(data) > 0, f"Фильтр вернул пустой список: {data}"
            assert all("bookingid" in item for item in data), (
                f"Не у всех элементов есть bookingid: {data}"
            )

        with allure.step("Проверяем, что созданная бронь есть в выдаче"):
            returned_ids = [item["bookingid"] for item in data]
            assert booking["id"] in returned_ids, (
                f"Бронь {booking['id']} не найдена. Полученные id: {returned_ids}"
            )

        with allure.step("Проверяем, что у всех найденных броней lastname='Brown'"):
            for item in data:
                booking_response = api_client.get_booking(item["bookingid"])
                assert booking_response.status_code == 200
                assert booking_response.json()["lastname"] == "Brown"