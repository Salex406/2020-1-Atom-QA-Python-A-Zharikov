import pytest
from selenium import webdriver
from ui.pages.login import LoginPage
from ui.pages.main import MainPage
from ui.pages.register import RegisterPage
from db.mysql_orm_client import MysqlOrmConnection
from db.orm_builder import MysqlOrmBuilder
from db.orm_model import User
from api_client import ApiClient
import allure
import time


class UsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def api():
    return ApiClient()

@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture(scope='function')
def register_page(driver):
    lp = LoginPage(driver)
    lp.click(lp.locators.BUTTON_REGISTER)
    return RegisterPage(driver)

@pytest.fixture(scope='function')
def main_page(driver):
    mp = MainPage(driver)
    NAME = mp.generate_data()
    user = User(username=NAME,
                password=NAME,
                email=NAME + "@test.tuu")
    connection = MysqlOrmConnection("test_qa", "qa_test", "BACK")
    builder = MysqlOrmBuilder(connection)
    builder.add_user(user)
    mp = MainPage(driver)
    mp.send(mp.locators.FORM_LOGIN, NAME)
    mp.send(mp.locators.FORM_PASSWORD, NAME)
    mp.click(mp.locators.BUTTON_LOGIN)
    yield mp
    builder.del_user(user)

@pytest.fixture(scope='function')
def driver(request):
    url = "http://192.168.0.254:80"
    capabilities = {
            "browserName": "chrome",
            "version": "81.0",
            "enableVNC": True,
            "enableVideo": False
    }
    driver = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub",
                              desired_capabilities=capabilities)
    driver.get(url)
    driver.maximize_window()
    yield driver
    if request.node.rep_call.failed:
        try:
            time.sleep(0.5)
            allure.attach(driver.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)
        except:
            pass
    driver.quit()
