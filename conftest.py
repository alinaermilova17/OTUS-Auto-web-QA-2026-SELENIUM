import platform
import pytest
import datetime
import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions

log_level = "DEBUG"


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome',
                     help='Browser: chrome or firefox')
    parser.addoption('--browser_version', action='store', default='128.0',
                     help='Browser version for remote executor')
    parser.addoption('--executor', action='store', default='local',
                     help='Executor: local or selenoid')
    parser.addoption('--executor_url', action='store',
                     default='http://localhost:4444/wd/hub',
                     help='Remote executor URL')
    parser.addoption('--headed', action='store_true', default=False,
                     help='Run browser in headed mode')
    parser.addoption('--url', action='store',
                     default=os.getenv('URL', 'http://localhost:8081'),
                     help="Base URL for PrestaShop")


@pytest.fixture(scope='function')
def browser(request):
    logger = logging.getLogger(__name__)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    file_handler = logging.FileHandler(f'logs/{request.node.name}.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info('===> Test started at %s' % datetime.datetime.now())
    logger.info('===> Test name: %s' % request.node.name)

    browser_name = request.config.getoption('--browser')
    browser_version = request.config.getoption('--browser_version')
    executor = request.config.getoption('--executor')
    executor_url = request.config.getoption('--executor_url')
    headed = request.config.getoption('--headed')
    url = request.config.getoption('--url')

    logger.info(f'Browser: {browser_name}, Version: {browser_version}, '
                f'Headed: {headed}, Executor: {executor}, URL: {url}')

    # Общие настройки для всех браузеров
    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-notifications')
        if not headed:
            options.add_argument('--headless=new')
    elif browser_name == 'firefox':
        options = FFOptions()
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        if not headed:
            options.add_argument('--headless')
    else:
        raise ValueError(f'Browser {browser_name} not supported')

    if executor == 'selenoid':
        # ===== Удаленный запуск (Selenoid / Selenium Grid) =====
        logger.info(f'Connecting to remote executor: {executor_url}')

        options.set_capability('browserVersion', browser_version)
        options.set_capability('selenoid:options', {
            'enableVNC': True,
            'enableVideo': False,
            'sessionTimeout': '5m'
        })

        driver = webdriver.Remote(
            command_executor=executor_url,
            options=options
        )
        logger.info(f'Remote session created at {executor_url}')

    elif executor == 'local':
        # ===== Локальный запуск =====
        logger.info(f'Starting local {browser_name}')

        if browser_name == 'chrome':
            driver = webdriver.Chrome(options=options)
        elif browser_name == 'firefox':
            driver = webdriver.Firefox(options=options)

        logger.info(f'Local driver created: {browser_name}')

    else:
        raise ValueError(f'Unknown executor: {executor}. Use "local" or "selenoid"')

    driver.maximize_window()
    driver.url = url
    driver.implicitly_wait(10)

    # Проверка доступности PrestaShop
    logger.info(f'Checking PrestaShop at {url}')
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            driver.get(url)
            time.sleep(2)
            if 'PrestaShop' in driver.title or 'prestashop' in driver.title.lower():
                logger.info(f'PrestaShop available: {driver.title}')
                break
        except Exception as e:
            logger.info(f'Attempt {attempt + 1}/{max_attempts}: {str(e)[:50]}...')
            time.sleep(2)
    else:
        logger.error(f'PrestaShop not available after {max_attempts} attempts')

    logger.info(f'Opened {url} in {browser_name}')
    logger.info(f'Page title: {driver.title}')

    driver.logger = logger

    yield driver

    logger.info('===> Test finished, closing browser')
    driver.quit()
    file_handler.close()
    logger.removeHandler(file_handler)


@pytest.fixture(scope='function')
def base_url(request):
    return request.config.getoption('--url')