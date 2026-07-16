import time

import pytest

from utils.driver_factory import create_android_driver

PKG = "weather.forecast.rain.radar"


def _scroll_to_top(driver):
    """메인 화면 맨 위로 스크롤합니다."""
    size = driver.get_window_size()
    for _ in range(5):
        driver.swipe(
            size["width"] // 2,
            int(size["height"] * 0.3),
            size["width"] // 2,
            int(size["height"] * 0.7),
            500,
        )
        time.sleep(0.3)


def _ensure_main_screen(driver):
    """메인 화면이 아니면 back으로 돌아간 뒤 상단으로 스크롤합니다."""
    main_activity = ".feature.home.ui.WeatherContentsActivity"
    for _ in range(5):
        current = driver.current_activity
        if current and main_activity.endswith(current.split(".")[-1]):
            break
        driver.back()
        time.sleep(0.5)
    _scroll_to_top(driver)
    time.sleep(0.5)


@pytest.fixture(scope="session")
def driver(request):
    """Appium 드라이버 세션을 생성하고 테스트 종료 후 정리합니다.

    잠금 화면 테스트만 실행할 경우 Appium 세션을 생성하지 않습니다.
    """
    collected = [item.nodeid for item in request.session.items]
    if all("lockscreen" in nid for nid in collected):
        yield None
        return
    d = create_android_driver()
    time.sleep(3)
    _scroll_to_top(d)
    time.sleep(1)
    yield d
    d.quit()


@pytest.fixture(autouse=True)
def ensure_main_screen(request, driver):
    """각 테스트 전에 메인 화면으로 돌아갑니다. (잠금 화면 테스트 제외)"""
    if "lockscreen" in request.node.nodeid:
        yield
        return
    _ensure_main_screen(driver)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 결과를 저장하고 스크린샷을 Allure에 첨부합니다."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        try:
            import allure
            name = f"FAIL_{item.name}" if rep.failed else f"PASS_{item.name}"
            if "lockscreen" in item.nodeid:
                from utils.adb_helper import take_screenshot
                import tempfile, os
                tmp = tempfile.mktemp(suffix=".png")
                take_screenshot(tmp)
                with open(tmp, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=name,
                        attachment_type=allure.attachment_type.PNG,
                    )
                os.unlink(tmp)
            else:
                driver = item.funcargs.get("driver")
                if driver:
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=name,
                        attachment_type=allure.attachment_type.PNG,
                    )
        except Exception:
            pass
