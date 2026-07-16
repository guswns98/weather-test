"""P2 Lock Screen Tests - 잠금 화면 날씨 표시 검증 (adb 기반).

Appium 세션 없이 adb + uiautomator dump 기반으로 동작합니다.
화면을 끄고 다시 켜서 잠금 화면 상태에서 날씨 요소를 검증합니다.
"""
import re
import time

import pytest

from utils.adb_helper import (
    dump_ui,
    find_elements_by_resource_id,
    is_screen_on,
    turn_screen_off,
    turn_screen_on,
)


@pytest.fixture(scope="module")
def lockscreen_ui():
    """모듈 단위로 한 번만 잠금 화면 UI를 덤프합니다."""
    turn_screen_off()
    time.sleep(2)
    turn_screen_on()
    time.sleep(3)
    root = dump_ui()
    yield root
    # teardown: 화면 켜고 잠금 해제 (스와이프)
    if not is_screen_on():
        turn_screen_on()
    import subprocess
    subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_MENU"], timeout=5)
    time.sleep(1)


class TestLockScreen:
    """잠금 화면에서 날씨 정보가 정상 표시되는지 검증합니다."""

    def test_lockscreen_temperature_displayed(self, lockscreen_ui):
        """잠금 화면에 현재 온도가 표시되는지 확인합니다."""
        elements = find_elements_by_resource_id(lockscreen_ui, "tv_weather_temperature")
        assert len(elements) > 0, "잠금 화면에 온도가 표시되지 않음"
        temp_text = elements[0].get("text", "")
        assert temp_text.strip(), "온도 값이 비어있음"

    def test_lockscreen_temperature_valid_range(self, lockscreen_ui):
        """잠금 화면 온도가 유효 범위(-50~60) 내인지 검증합니다."""
        elements = find_elements_by_resource_id(lockscreen_ui, "tv_weather_temperature")
        assert len(elements) > 0, "잠금 화면에 온도가 표시되지 않음"
        temp_text = elements[0].get("text", "")
        match = re.search(r"-?\d+", temp_text)
        assert match, f"온도에서 숫자를 추출할 수 없음: {temp_text}"
        temp = int(match.group())
        assert -50 <= temp <= 60, f"온도가 유효 범위를 벗어남: {temp}도"

    def test_lockscreen_weather_status_displayed(self, lockscreen_ui):
        """잠금 화면에 날씨 상태(맑음/흐림 등)가 표시되는지 확인합니다."""
        elements = find_elements_by_resource_id(lockscreen_ui, "tv_weather_text")
        assert len(elements) > 0, "잠금 화면에 날씨 상태가 표시되지 않음"
        status_text = elements[0].get("text", "")
        assert status_text.strip(), "날씨 상태 값이 비어있음"

    def test_lockscreen_high_low_temperature(self, lockscreen_ui):
        """잠금 화면에 최고/최저 온도가 표시되는지 확인합니다."""
        max_els = find_elements_by_resource_id(lockscreen_ui, "tv_weather_max_temperature")
        min_els = find_elements_by_resource_id(lockscreen_ui, "tv_weather_min_temperature")
        assert len(max_els) > 0, "최고 온도가 표시되지 않음"
        assert len(min_els) > 0, "최저 온도가 표시되지 않음"
        assert max_els[0].get("text", "").strip(), "최고 온도 값이 비어있음"
        assert min_els[0].get("text", "").strip(), "최저 온도 값이 비어있음"

    def test_lockscreen_yesterday_compare(self, lockscreen_ui):
        """잠금 화면에 어제 대비 온도 비교가 표시되는지 확인합니다."""
        elements = find_elements_by_resource_id(lockscreen_ui, "tv_weather_temperature_compare")
        assert len(elements) > 0, "어제 대비 온도가 표시되지 않음"
        text = elements[0].get("text", "")
        assert "어제" in text, f"어제 대비 정보가 아님: {text}"

    def test_lockscreen_sensible_temperature(self, lockscreen_ui):
        """잠금 화면에 체감온도가 표시되는지 확인합니다."""
        elements = find_elements_by_resource_id(lockscreen_ui, "tv_weather_sensible_temperature")
        assert len(elements) > 0, "체감온도가 표시되지 않음"
        text = elements[0].get("text", "")
        assert "체감" in text, f"체감온도 정보가 아님: {text}"

