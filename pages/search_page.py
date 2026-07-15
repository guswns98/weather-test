from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

PKG = "weather.forecast.rain.radar"


class SearchPage(BasePage):
    """지역 검색 화면 Page Object."""

    LOC_SEARCH_INPUT = (AppiumBy.CLASS_NAME, "android.widget.EditText")

    def search_location(self, keyword: str):
        search_input = self.find(*self.LOC_SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(keyword)

    def tap_first_result(self):
        """검색 결과 첫 번째 항목을 탭합니다."""
        results = self.finds(AppiumBy.CLASS_NAME, "android.widget.TextView")
        clickable_results = [r for r in results if r.text and r.text != ""]
        if clickable_results:
            clickable_results[0].click()

    def go_back(self):
        """Android 백 버튼으로 뒤로가기."""
        self.driver.back()
