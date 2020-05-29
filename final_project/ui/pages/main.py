from selenium.webdriver.common.keys import Keys
from ui.pages.base import BasePage
from ui.locators.locators import MainPageLocators
from ui.locators.locators import LoginPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()
