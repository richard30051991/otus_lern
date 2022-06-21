from pages.page_autorization import authorization_admin
import datetime
from pathlib import Path
import allure
import pytest
from selenium import webdriver
import logging
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
import os
import time

fixture_authorization = authorization_admin
DRIVERS = os.getenv('DRIVERS')


def directory_log():
    path = (Path.cwd() / "logs")
    if os.path.exists(path):
        print("Директория найдена")
    else:
        os.mkdir(path)
        print("Директория создана")
    return path


logging.basicConfig(handlers=[logging.FileHandler(filename=directory_log() / "test.log", encoding='utf-8')],
                    datefmt="%F %A %T",
                    format="[%(asctime)s] %(name)s:%(levelname)s:%(message)s",
                    level=logging.INFO)


class MyListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        logging.info(f"I'm navigating to {url} and {driver.title}")

    def after_navigate_to(self, url, driver):
        logging.info(f"I'm on {url}")

    def before_navigate_back(self, driver):
        logging.info(f"I'm navigating back")

    def after_navigate_back(self, driver):
        logging.info(f"I'm back!")

    def before_find(self, by, value, driver):
        logging.info(f"I'm looking for '{value}' with '{by}'")

    def after_find(self, by, value, driver):
        logging.info(f"I've found '{value}' with '{by}'")

    def before_click(self, element, driver):
        logging.info(f"I'm clicking {element}")

    def after_click(self, element, driver):
        logging.info(f"I've clicked {element}")

    def before_execute_script(self, script, driver):
        logging.info(f"I'm executing '{script}'")

    def after_execute_script(self, script, driver):
        logging.info(f"I've executed '{script}'")

    def before_quit(self, driver):
        logging.info(f"I'm getting ready to terminate {driver}")

    def after_quit(self, driver):
        logging.info(f"WASTED!!!")

    def on_exception(self, exception, driver):
        logging.error(f'Oooops i got: {exception}')
        driver.save_screenshot(f'logs/{driver.session_id}.png')


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser type: chrome or firefox or Opera.")
    parser.addoption("--versions", action="store", default="100.0")
    parser.addoption("--url", action="store", default="http://192.168.192.149:8180/")
    parser.addoption("--executor", default="127.0.0.1")
    parser.addoption("--log_level", action="store", default="DEBUG")
    parser.addoption("--mobile", action="store_true")


@pytest.fixture(scope="function")
def browser(request):
    """Запуск / выбор и закрытие браузера"""
    current_date = datetime.datetime.now()
    browsers = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    log_level = request.config.getoption("--log_level")
    version = request.config.getoption("--versions")
    mobile = request.config.getoption("--mobile")
    logger = logging.getLogger('driver')
    test_name = request.node.name
    logger.setLevel(level=log_level)
    logger.info("===> Test {} started at {}".format(test_name, datetime.datetime.now()))
    print(f"--browser: {browsers}, {current_date}")
    driver, options = None, None
    if executor == "local":
        caps = {'goog:chromeOptions': {}}

        if mobile:
            caps["goog:chromeOptions"]["mobileEmulation"] = {"deviceName": "iPhone 5/SE"}
            driver = webdriver.Chrome(desired_capabilities=caps)
        elif browsers == 'chrome':
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=options, executable_path=f"{DRIVERS}/chromedriver",
                                      desired_capabilities=caps)
        elif browsers == 'firefox':
            driver = webdriver.Firefox(options=options, executable_path=f"{DRIVERS}/geckodriver",
                                       desired_capabilities=caps)
        elif browsers == 'opera':
            driver = webdriver.Opera(options=options, executable_path=f"{DRIVERS}/operachromiumdriver",
                                     desired_capabilities=caps)
        else:
            print("unrecognized --browser: {}".format(browsers))
            yield None
    else:
        executor_url = f"http://{executor}:4444/wd/hub"

        caps = {
            "browserName": browsers,
            "browserVersion": version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False,
            },
            'acceptSslCerts': True,
            'acceptInsecureCerts': True,
            'goog:chromeOptions': {}
        }

        if browsers == "chrome" and mobile:
            caps["goog:chromeOptions"]["mobileEmulation"] = {"deviceName": "iPhone 5/SE"}

        driver = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=caps
        )

        if not mobile:
            driver.maximize_window()
    driver = EventFiringWebDriver(driver, MyListener())
    driver.test_name = request.node.name
    driver.log_level = log_level
    logger.info(driver)

    driver.maximize_window()
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(6)
    yield driver
    driver.quit()
    logger.info("===> Test {} finished at {}".format(test_name, datetime.datetime.now()))


@pytest.fixture(scope="function")
def url(request):
    urls = request.config.getoption("--url")
    yield urls


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    current_date = datetime.datetime.now()
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed or rep.skipped:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode):
                if 'browser' in item.fixturenames:
                    web_driver = item.funcargs['browser']
                else:
                    print('Fail to take screen-shot')
                    return
            time.sleep(2)
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name=f'screenshot {current_date}',
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))
