import requests
import allure
from tests_selenium.api.config_api import BASE_API_URL


class BaseApi:
    def __init__(self):
        self.base_url = BASE_API_URL
        self.session = requests.Session()

    @allure.step("GET {path}")
    def get(self, path, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    @allure.step("POST {path}")
    def post(self, path, **kwargs):
        return self.session.post(f"{self.base_url}{path}", **kwargs)

    @allure.step("PUT {path}")
    def put(self, path, **kwargs):
        return self.session.put(f"{self.base_url}{path}", **kwargs)

    @allure.step("PATCH {path}")
    def patch(self, path, **kwargs):
        return self.session.patch(f"{self.base_url}{path}", **kwargs)

    @allure.step("DELETE {path}")
    def delete(self, path, **kwargs):
        return self.session.delete(f"{self.base_url}{path}", **kwargs)

    def attach_response(self, response, name="response"):
        allure.attach(
            response.text,
            name=f"{name} [{response.status_code}]",
            attachment_type=allure.attachment_type.JSON
            if "application/json" in response.headers.get("Content-Type", "")
            else allure.attachment_type.TEXT
        )