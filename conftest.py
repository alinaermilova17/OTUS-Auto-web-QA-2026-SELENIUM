import platform
import pytest
import datetime
import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.options import Options as FFOptions

log_level = "DEBUG"


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome',
                     help='Browser to run tests: chrome or firefox')
    parser.addoption('--browser_version', action='store', default='128.0',
                     help='Browser version')
    parser.addoption('--executor', action='store', default='selenoid',
                     help='Executor: selenoid or local')
    parser.addoption('--executor_url', action='store',
                     default=os.getenv('EXECUTOR_URL','http://selenium-chrome:4444/wd/hub'),
                     help='Executor URL')
    parser.addoption('--headed', action='store_true', default=False,
                     help='Run browser in headed mode')
    parser.addoption('--url', action='store',
                     default=os.getenv('URL', 'http://prestashop:80'),
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

    logger.info(f'Browser: {browser_name}, Version: {browser_version}, Headed: {headed}, Executor: {executor}, URL: {url}')

    if executor == 'selenoid':
        if browser_name == 'chrome':
            options = ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')

            if not headed:
                options.add_argument('--headless=new')

        elif browser_name == 'firefox':
            options = FFOptions()
            options.add_argument('--width=1920')
            options.add_argument('--height=1080')

            if not headed:
                options.add_argument('--headless')

        else:
            raise ValueError(f'Unsupported browser: {browser_name}')

        driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            options=options
        )
        logger.info(f'Remote session created successfully at {executor_url}')

    else:
        logger.info(f'Creating local driver: {browser_name}')

        if browser_name == 'chrome':
            options = ChromeOptions()
            if not headed:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')

            driver = webdriver.Chrome(options=options)

        elif browser_name == 'firefox':
            options = FFOptions()
            if not headed:
                options.add_argument('--headless')
            options.add_argument('--width=1920')
            options.add_argument('--height=1080')

            if '24.04' in platform.version():
                service = FFService(executable_path="/snap/bin/geckodriver")
            else:
                service = FFService()
            driver = webdriver.Firefox(options=options, service=service)
        else:
            driver = webdriver.Safari()

    driver.maximize_window()
    driver.url = url
    driver.implicitly_wait(10)

    logger.info(f'Проверка доступности PrestaShop по адресу {url}')
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            driver.get(url)
            time.sleep(2)
            if 'PrestaShop' in driver.title or 'prestashop' in driver.title.lower():
                logger.info(f'PrestaShop доступен: {driver.title}')
                break
        except Exception as e:
            logger.info(f'Попытка {attempt + 1}/{max_attempts}: {str(e)[:50]}...')
            time.sleep(2)
    else:
        logger.error(f'PrestaShop не доступен после {max_attempts} попыток')

    logger.info(f'Opened {url} in {browser_name}')
    logger.info(f'Page title: {driver.title}')

    driver.logger = logger

    yield driver

    logger.info('===> Test finished, closing browser')
    driver.quit()
    file_handler.close()
    logger.removeHandler(file_handler)