import pytest
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from tests.base import BaseCase


class Test(BaseCase):
    # @pytest.mark.skip(reason='WORKS')
    @pytest.mark.UI
    def test_login_negative(self, driver):
        self.main.authorize('qa_python_mail@ro.ro', 'wrong')
        assert "Invalid login or password" in self.driver.page_source

    # @pytest.mark.skip(reason='WORKS')
    @pytest.mark.UI
    def test_login_positive(self, authorize):
        EMAIL = "qa_python_mail@ro.ru"
        self.cabinet = authorize
        assert EMAIL in self.driver.page_source

    # @pytest.mark.skip(reason='WORKS')
    @pytest.mark.UI
    def test_create_campaign(self, authorize):
        self.cabinet = authorize
        site_name = "http://test.ru"
        camp_name = "TEST_CAMP"
        self.cabinet.create_campaign(site_name, camp_name)
        self.cabinet.find((By.XPATH, self.cabinet.locators.CAMPAIGN.format(camp_name)))
        self.cabinet.click((By.XPATH, self.cabinet.locators.CHKBX_CREATED_CAMPAIGN.format(
            camp_name)))
        self.base.click(self.cabinet.locators.BUTTON_ACTIONS)
        self.base.click(self.cabinet.locators.BUTTON_DELETE)

    # @pytest.mark.skip(reason='WORKS')
    @pytest.mark.UI
    def test_create_segment(self, authorize):
        self.cabinet = authorize
        name = 'TEST_SEGMENT'
        self.segment.create_segment(name)
        assert name in self.driver.page_source
        self.segment.delete_segment(name)

    # @pytest.mark.skip(reason='WORKS')
    @pytest.mark.UI
    def test_create_delete_segment(self, authorize):
        self.cabinet = authorize
        name = 'TEST_SEGMENT_CR_DEL'
        self.segment.create_segment(name)
        self.segment.delete_segment(name)
