"""P1 Smoke Tests - 첫화면 날씨 핵심 기능 검증."""
import re

import pytest

from pages.main_page import MainPage


class TestSmoke:
    """앱 실행 후 메인 화면 핵심 요소가 정상 표시되는지 확인합니다."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.main = MainPage(driver)

    def test_main_screen_loads(self):
        """메인 화면의 현재 날씨 정보 영역이 로딩되는지 확인합니다."""
        assert self.main.is_weather_info_displayed(), "현재 날씨 정보 영역이 표시되지 않음"

    def test_current_temperature_valid_range(self):
        """현재 온도가 유효한 범위(-50~60) 내로 표시되는지 확인합니다."""
        temp_desc = self.main.get_current_temperature()  # e.g. "현재 온도 26도"
        match = re.search(r"-?\d+", temp_desc)
        assert match, f"온도를 파싱할 수 없음: {temp_desc}"
        temp_value = int(match.group())
        assert -50 <= temp_value <= 60, f"온도 값이 유효 범위를 벗어남: {temp_value}"

    def test_weather_status_displayed(self):
        """날씨 상태 및 체감온도가 표시되는지 확인합니다."""
        status = self.main.get_weather_status_text()
        assert len(status) > 0, "날씨 상태 텍스트가 비어 있음"
        assert "체감" in status, f"체감온도 정보가 없음: {status}"

    def test_yesterday_compare_displayed(self):
        """어제 대비 온도 비교 정보가 표시되는지 확인합니다."""
        assert self.main.is_yesterday_compare_displayed(), "어제 대비 비교 정보가 표시되지 않음"
        text = self.main.get_yesterday_compare_text()
        assert "어제" in text, f"어제 비교 텍스트가 올바르지 않음: {text}"

    def test_high_low_temperature(self):
        """최고/최저 온도가 표시되는지 확인합니다."""
        high_low = self.main.get_high_low_temp()  # e.g. "최고 29° 최저 23°"
        assert "최고" in high_low and "최저" in high_low, f"최고/최저 온도 표시 오류: {high_low}"

    def test_life_info_cards_displayed(self):
        """미세먼지, 바람, 습도, 강수확률 카드가 표시되는지 확인합니다."""
        cards = self.main.get_life_info_cards()
        card_names = [c["name"] for c in cards]
        assert "미세먼지" in card_names, f"미세먼지 카드 없음: {card_names}"
        assert "습도" in card_names, f"습도 카드 없음: {card_names}"
        assert "강수확률" in card_names, f"강수확률 카드 없음: {card_names}"
        # 값이 비어있지 않은지 확인
        for card in cards:
            assert card["value"], f"{card['name']} 카드 값이 비어 있음"
