import os
import platform
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.chrome.options import Options


def setup_logging():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(f'{log_dir}/test.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

setup_logging()
logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def browser():
    logger.info(' Запуск браузера')

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    logger.info(' Браузер запущен')
    yield driver

    logger.info(' Закрытие браузера')
    driver.quit()
    logger.info(' Браузер закрыт')

def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome')
    parser.addoption('--url', action='store', default='http://localhost:8081/')


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption('--browser')
    url = request.config.getoption('--url')

    if browser_name == 'chrome':
        driver = webdriver.Chrome(service=ChromiumService())
    elif browser_name == 'firefox':
        if '24.04' in platform.version():
            service = FFService(executable_path='/snap/bin/geckodriver')
        else:
            service = FFService()
        driver = webdriver.Firefox(options=FFOptions(), service=service)
    else:
        driver = webdriver.Safari()

    driver.maximize_window()
    driver.url = url
    request.addfinalizer(driver.close)

    return driver


