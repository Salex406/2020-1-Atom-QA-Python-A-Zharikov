from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
import random
from db.orm_model import User
import string


RETRY_COUNT = 3


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        random.seed()
        NAME = self.generate_data()
        user = User(
            username = NAME,
            password = NAME,
            email = NAME + "@test.tuu"
        )
        self.user = user
        
        
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def clear_form(self, locator, timeout=None):
        self.wait(timeout).until((EC.element_to_be_clickable(locator))).clear()

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 8
        return WebDriverWait(self.driver, timeout=timeout)

    def click(self, locator, timeout=None):
        for i in range(RETRY_COUNT):
            try:
                self.find(locator)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                self.scroll_to_element(element)
                element.click()
                return

            except StaleElementReferenceException:
                if i < RETRY_COUNT - 1:
                    pass
        raise

    def send(self, locator, message, timeout=None):
        self.wait(timeout).until((EC.element_to_be_clickable(locator))).send_keys(message)

    def scroll_to_element(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def check_required(self, locator):
        form = self.find(locator)
        return form.get_attribute("required")

    def check_minlength(self, locator):
        form = self.find(locator)
        return form.get_attribute("minlength")
    
    def generate_data(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def get_user(self):
        return self.user
