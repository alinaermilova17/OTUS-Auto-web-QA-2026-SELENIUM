import allure
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, timeout=10):
        self.browser = browser
        self.wait = WebDriverWait(browser, timeout)
        self.logger = browser.logger
        self.class_name = type(self).__name__

    @allure.step('Открыть страницу: {url}')
    def open(self, url):
        self.logger.info('| Class: %s | Opening url: %s' % (self.class_name, url))
        return self.browser.get(url)

    @allure.step('Найти элемент: {locator}')
    def find(self, locator):
        self.logger.info(
            (
                    '| Class: %s | Check if elements %s is present'
                    % (self.class_name, str(locator))
            )
        )
        try:
            return self.browser.find_element(*locator)
        except NoSuchElementException:
            allure.attach(
                body=self.browser.get_screenshot_as_png(),
                name='screenshot.png',
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f'Element with locator:{locator} is absent on page {self.browser.current_url}')

    @allure.step('Дождаться видимости элемента: {locator}')
    def wait_visible(self, locator,timeout=10):
        self.logger.debug(
            '| Class: %s | Wait %s sec for element: %s'
            % (self.class_name, str(timeout), str(locator))
        )
        try:
            return self.wait.until( EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.browser.save_screenshot(f"{self.browser.session_id}.png")
            raise AssertionError(f"Didn't wait for: {locator}")

    @allure.step('Дождаться кликабельности элемента: {locator}')
    def wait_clickable(self, locator):
        self.logger.info(
            (
                    '| Class: %s | Check if elements %s is с clickable'
                    % (self.class_name, str(locator))
            )
        )
        try:
            return self.wait.until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            self.browser.save_screenshot(f'{self.browser.session_id}.png')
            raise AssertionError(f"Didn't wait for: {locator}")

    @allure.step('Кликнуть по элементу: {locator}')
    def click(self, locator):
        self.logger.debug("%s: Clicking element: %s" % (self.class_name, str(locator)))
        self.wait_clickable(locator).click()

    @allure.step('Получить атрибут : {attribute_name}')
    def get_attribute(self, locator, attribute_name):
        self.logger.debug('Get attribute_name from element: %s' % str(locator))
        return self.wait_visible(locator).get_attribute(attribute_name)

    @allure.step('Элемент {locator} показан на странице')
    def is_visible(self, locator) -> bool:
        return self.wait_visible(locator).is_displayed()



