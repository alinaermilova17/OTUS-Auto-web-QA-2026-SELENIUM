import allure
from api_clients.base_api import BaseApi


class BookingApi(BaseApi):

    @allure.step("Создать токен")
    def create_token(self, username="admin", password="password123"):
        payload = {"username": username, "password": password}
        response = self.post("/auth", json=payload)
        self.attach_response(response)
        return response

    @allure.step("Получить все ID броней")
    def get_all_bookings(self, params=None):
        response = self.get("/booking", params=params)
        self.attach_response(response)
        return response

    @allure.step("Получить бронь по ID: {booking_id}")
    def get_booking(self, booking_id):
        response = self.get(f"/booking/{booking_id}")
        self.attach_response(response)
        return response

    @allure.step("Создать бронь")
    def create_booking(self, payload):
        response = self.post("/booking", json=payload)
        self.attach_response(response)
        return response

    @allure.step("Обновить бронь (PUT) ID: {booking_id}")
    def update_booking(self, booking_id, payload, token=None):
        headers = {"Cookie": f"token={token}"} if token else {}
        response = self.put(f"/booking/{booking_id}", json=payload, headers=headers)
        self.attach_response(response)
        return response

    @allure.step("Частично обновить бронь (PATCH) ID: {booking_id}")
    def patch_booking(self, booking_id, payload, token=None):
        headers = {"Cookie": f"token={token}"} if token else {}
        response = self.patch(f"/booking/{booking_id}", json=payload, headers=headers)
        self.attach_response(response)
        return response

    @allure.step("Удалить бронь ID: {booking_id}")
    def delete_booking(self, booking_id, token=None):
        headers = {"Cookie": f"token={token}"} if token else {}
        response = self.delete(f"/booking/{booking_id}", headers=headers)
        self.attach_response(response)
        return response