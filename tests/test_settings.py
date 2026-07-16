"""P3 Settings Tests - 메뉴/설정 화면 검증."""
import time

import pytest

from pages.main_page import MainPage


class TestSettings:
    """메뉴 화면 진입을 검증합니다."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.main = MainPage(driver)
        self._menu_opened = False
        yield
        # teardown: 메뉴가 열린 경우에만 back으로 닫기
        if self._menu_opened:
            self.driver.back()
            time.sleep(0.5)

    def test_open_menu(self):
        """메뉴 화면이 정상적으로 열리는지 확인합니다."""
        self.main.tap_menu()
        self._menu_opened = True
        time.sleep(1)
