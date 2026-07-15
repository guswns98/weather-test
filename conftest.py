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
    """메인 화면 상단으로 스크롤합니다."""
    _scroll_to_top(driver)
    time.sleep(0.5)


@pytest.fixture(scope="session")
def driver():
    """Appium 드라이버 세션을 생성하고 테스트 종료 후 정리합니다."""
    d = create_android_driver()
    time.sleep(3)
    _scroll_to_top(d)
    time.sleep(1)
    yield d
    d.quit()


@pytest.fixture(autouse=True)
def ensure_main_screen(driver):
    """각 테스트 전에 메인 화면으로 돌아갑니다."""
    _ensure_main_screen(driver)
    yield


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    """테스트 실패 시 스크린샷을 자동 저장합니다."""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            allure = pytest.importorskip("allure")
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"failure_{request.node.name}",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 결과를 request.node 에 저장합니다."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
