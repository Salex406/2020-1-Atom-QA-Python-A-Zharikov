import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ui.pages.base import BasePage
from ui.pages.main import MainPage
from ui.pages.cabinet import CabinetPage
from ui.pages.segment import SegmentPage
from selenium.webdriver.common.keys import Keys
from api.client import MytargetClient


class UsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def cabinet_page(driver, config):
    return CabinetPage(driver, config)


@pytest.fixture(scope='function')
def base_page(driver, config):
    return BasePage(driver, config)


@pytest.fixture(scope='function')
def segment_page(driver, config):
    return SegmentPage(driver, config)


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    url = config['url']
    selenoid = config['selenoid']

    if browser == 'chrome':
        if selenoid == "True":
            options = ChromeOptions()
            options.add_argument("--window-size=800,600")
            capabilities = {'acceptInsecureCerts': True,
                        'browserName': 'chrome',
                        'version': version,
                        }

            driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub/',
                                  options=options,
                                  desired_capabilities=capabilities
                                  )
        else:   
            manager = ChromeDriverManager(version='latest')
            driver = webdriver.Chrome(executable_path=manager.install())
    elif browser == 'firefox':
        manager = GeckoDriverManager(version=version)
        driver = webdriver.Firefox(executable_path=manager.install())

    else:
        raise UsupportedBrowserException(f'Usupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.fixture(scope='function')
def main_page(driver, config):
    return MainPage(driver, config)


@pytest.fixture(scope='function')
def authorize(driver, config):
    bp = BasePage(driver, config)
    bp.click(MainPage.locators.BUTTON_LOGIN)
    bp.send(MainPage.locators.FORM_EMAIL, "qa_python_mail@ro.ru")
    bp.send(MainPage.locators.FORM_PASSWORD, "pmQ3yMi1")
    bp.send(MainPage.locators.FORM_PASSWORD, Keys.RETURN)
    return CabinetPage(driver, config)

@pytest.fixture(scope='function')
def Mytarget_api():
    user = 'qa_python_mail@ro.ru'
    password = "pmQ3yMi1"
    return MytargetClient(user, password)
