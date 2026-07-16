"""P2 Search Tests - 지역 검색 기능 검증."""
import time

import pytest

from pages.main_page import MainPage
from pages.search_page import SearchPage


class TestSearch:
    """지역 검색 기능이 정상 동작하는지 검증합니다."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.main = MainPage(driver)
        self.search = SearchPage(driver)
        self._search_opened = False
        yield
        if self._search_opened:
            self.driver.back()
            time.sleep(0.5)

    def test_open_search(self):
        """검색 화면이 정상적으로 열리는지 확인합니다."""
        self.main.tap_search()
        self._search_opened = True
        time.sleep(1)
        assert self.search.is_displayed(*self.search.LOC_SEARCH_INPUT), "검색 입력창이 표시되지 않음"

    def test_search_location(self):
        """지역명 검색이 동작하는지 확인합니다."""
        self.main.tap_search()
        self._search_opened = True
        time.sleep(1)
        self.search.search_location("서울")
        time.sleep(2)
