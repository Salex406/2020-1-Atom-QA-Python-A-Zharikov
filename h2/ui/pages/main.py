from selenium.webdriver.common.keys import Keys
from ui.pages.base import BasePage
from ui.locators.locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()
    
    def authorize(self, email, password):
        self.click(self.locators.BUTTON_LOGIN)
        self.send(self.locators.FORM_EMAIL, email)
        self.send(self.locators.FORM_PASSWORD, password)
        self.send(self.locators.FORM_PASSWORD, Keys.RETURN)
    