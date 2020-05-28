from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from ui.pages.base import BasePage
from ui.locators.locators import RegisterPageLocators


class RegisterPage(BasePage):
    locators = RegisterPageLocators()
