"""P2 Weather Tests - 날씨 상세 기능 검증."""
import pytest

from pages.main_page import MainPage


class TestWeather:
    """단기예보 탭 전환 등 날씨 상세 기능을 검증합니다."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.main = MainPage(driver)

    def test_forecast_graph_displayed(self):
        """단기예보 그래프가 표시되는지 확인합니다."""
        self.main.scroll_down()
        assert self.main.is_forecast_graph_displayed(), "단기예보 그래프가 표시되지 않음"

    # TODO: 단기예보 탭 전환 테스트 - locator 검증 후 활성화
    # def test_forecast_tab_wind(self):
    #     """단기예보 바람 탭으로 전환되는지 확인합니다."""
    #     self.main.scroll_down()
    #     self.main.tap_forecast_tab_wind()
    #     assert self.main.is_forecast_graph_displayed(), "바람 탭 전환 후 그래프 미표시"

    # def test_forecast_tab_humidity(self):
    #     """단기예보 습도 탭으로 전환되는지 확인합니다."""
    #     self.main.scroll_down()
    #     self.main.tap_forecast_tab_humidity()
    #     assert self.main.is_forecast_graph_displayed(), "습도 탭 전환 후 그래프 미표시"

    # def test_forecast_tab_back_to_weather(self):
    #     """단기예보 날씨 탭으로 다시 전환되는지 확인합니다."""
    #     self.main.scroll_down()
    #     self.main.tap_forecast_tab_wind()
    #     self.main.tap_forecast_tab_weather()
    #     assert self.main.is_forecast_graph_displayed(), "날씨 탭 복귀 후 그래프 미표시"
