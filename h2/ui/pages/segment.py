from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from ui.pages.base import BasePage
from ui.locators.locators import SegmentPageLocators


class SegmentPage(BasePage):
    locators = SegmentPageLocators()

    def create_segment(self, name):
        self.click(self.locators.BUTTON_TO_SEGMENTS)
        try:
            button = self.click(self.locators.BUTTON_CREATE_SEGMENT_2)
        except TimeoutException:
            button = self.click(self.locators.BUTTON_CREATE_SEGMENT_1)
        self.clear_form(self.locators.SEGMENT_NAME)
        self.send(self.locators.SEGMENT_NAME, name)
        self.click(self.locators.ADD_SEGMENT)
        self.click(self.locators.BUTTON_APPS)
        self.click(self.locators.CHECKBOX_SEGM)
        self.click(self.locators.BUTTON_ADD_SEGMENT_1)
        self.click(self.locators.BUTTON_CREATE_SEGMENT_1)
        self.find((By.XPATH, self.locators.CREATED_SEGMENT.format(name)))

    def delete_segment(self, name):
        self.click(self.locators.BUTTON_TO_SEGMENTS)
        self.click((By.XPATH, self.locators.BUTTON_DELETE_SEGMENT.format(name)))
        self.click(self.locators.BUTTON_DELETE_CONFIRM)
        self.click(self.locators.BUTTON_TO_SEGMENTS)
