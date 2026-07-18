import allure
from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage


class HomePage(BasePage):
    MY_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[title='View my customer account']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a[href*='logout']")

    @allure.step('Пользователь залогинен')
    def is_user_logged_in(self) -> bool:
        has_account_link = self.is_visible(self.MY_ACCOUNT_LINK)
        self.is_visible(self.LOGOUT_BUTTON)
        return has_account_link

    @allure.step('Пользователь разлогинен')
    def logout(self):
        self.click(self.LOGOUT_BUTTON)

