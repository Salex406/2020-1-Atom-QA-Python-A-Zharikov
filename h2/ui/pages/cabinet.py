import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from ui.pages.base import BasePage
from ui.locators.locators import CabinetPageLocators


class CabinetPage(BasePage):
    locators = CabinetPageLocators()

    def create_campaign(self, site, campaign):
        self.click(self.locators. BUTTON_CREATE_CAMPAIGN)
        self.click(self.locators.BUTTON_SALEPOINTS)
        self.send(self.locators.FORM_SITE_NAME, site)
        self.clear_form(self.locators.FORM_CAMPAIGN_NAME)
        self.send(self.locators.FORM_CAMPAIGN_NAME, campaign)
        self.click(self.locators.SELECTOR_BANNER)

        form = self.find(self.locators.BUTTON_UPLOAD_PIC)
        form.send_keys(os.path.realpath((os.path.join(os.path.dirname(__file__), '..', '..', 'pic.jpg'))))
        self.click(self.locators.BUTTON_SUBMIT)
        self.click(self.locators.BUTTON_CREATE_C)
