import pytest
import os
from ui.pages.base import BasePage
from ui.pages.main import MainPage
from ui.pages.cabinet import CabinetPage
from ui.pages.segment import SegmentPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver = driver
        self.config = config
        self.base: BasePage = request.getfixturevalue('base_page')
        self.main: MainPage = request.getfixturevalue('main_page')
        self.cabinet: CabinetPage = request.getfixturevalue('cabinet_page')
        self.segment: SegmentPage = request.getfixturevalue('segment_page')
