import platform
import pytest
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.options import Options as FFOptions
import logging

log_level = "DEBUG"


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--url", action="store", default="http://localhost:8081/")


@pytest.fixture()
def browser(request):
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(f'logs/{request.node.name}.log')
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info('===> Test started at %s' % datetime.datetime.now())
    logger.info('===> Test name: %s' % request.node.name)

    browser_name = request.config.getoption('--browser')
    url = request.config.getoption('--url')

    if browser_name == 'chrome':
        driver = webdriver.Chrome(service=ChromiumService())
    elif browser_name == 'firefox':
        if '24.04' in platform.version():
            service = FFService(executable_path="/snap/bin/geckodriver")
        else:
            service = FFService()
        driver = webdriver.Firefox(options=FFOptions(), service=service)
    else:
        driver = webdriver.Safari()

    driver.maximize_window()
    driver.url = url
    logger.info(f'Opened {url} in {browser_name}')

    driver.logger = logger

    yield driver

    logger.info('===> Test finished, closing browser')
    driver.quit()
    file_handler.close()
    logger.removeHandler(file_handler)
