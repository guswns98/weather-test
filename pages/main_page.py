from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

PKG = "weather.forecast.rain.radar"


class MainPage(BasePage):
    """첫화면 날씨 메인 화면 Page Object."""

    # --- 상단 앱바 ---
    LOC_MENU_BTN = (AppiumBy.ACCESSIBILITY_ID, "메뉴 버튼")
    LOC_LOCATION_NAME = (AppiumBy.ANDROID_UIAUTOMATOR,
                         'new UiSelector().className("android.widget.TextView")'
                         '.resourceIdMatches("").textMatches(".+시.+|.+구.+|.+도.+")')
    LOC_SEARCH_BTN = (AppiumBy.ACCESSIBILITY_ID, "검색 버튼")

    # --- 현재 날씨 기본 정보 ---
    LOC_WEATHER_INFO_AREA = (AppiumBy.ACCESSIBILITY_ID, "현재 날씨 기본 정보 영역")
    LOC_CURRENT_TEMP = (AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().descriptionContains("현재 온도")')
    LOC_CURRENT_TEMP_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().descriptionContains("현재 온도")'
                            '.childSelector(new UiSelector().className("android.widget.TextView").index(0))')
    LOC_HIGH_LOW_TEMP = (AppiumBy.ANDROID_UIAUTOMATOR,
                         'new UiSelector().descriptionContains("최고")')
    LOC_YESTERDAY_COMPARE = (AppiumBy.ACCESSIBILITY_ID, "어제 대비 온도 변화")
    LOC_WEATHER_STATUS = (AppiumBy.ACCESSIBILITY_ID, "날씨 상태 및 체감온도")

    # --- 생활 정보 카드 (미세먼지, 바람, 습도, 강수확률) ---
    LOC_LIFE_INFO_CONTAINER = (AppiumBy.ID, f"{PKG}:id/card_life_info_container")
    LOC_LIFE_INFO_VALUE = (AppiumBy.ID, f"{PKG}:id/tv_life_info_value")
    LOC_LIFE_INFO_NAME = (AppiumBy.ID, f"{PKG}:id/tv_life_info_name")

    # --- 단기 예보 ---
    LOC_SHORT_FORECAST = (AppiumBy.ID, f"{PKG}:id/short_forecast_container")
    LOC_FORECAST_GRAPH = (AppiumBy.ACCESSIBILITY_ID, "단기예보 그래프")
    LOC_TAB_WEATHER = (AppiumBy.ANDROID_UIAUTOMATOR,
                       'new UiSelector().text("날씨")')
    LOC_TAB_WIND = (AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().text("바람")')
    LOC_TAB_HUMIDITY = (AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().text("습도")')

    # --- 액션 메서드 ---

    def get_location_name(self) -> str:
        # 앱바 중앙의 지역명 텍스트
        el = self.find(AppiumBy.ANDROID_UIAUTOMATOR,
                       'new UiSelector().descriptionMatches("")'
                       '.childSelector(new UiSelector().className("android.widget.TextView"))')
        # fallback: 앱바 영역에서 텍스트를 가진 TextView 찾기
        try:
            appbar = self.find(AppiumBy.ID, f"{PKG}:id/appbar_view_layout")
            texts = appbar.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for t in texts:
                if t.text:
                    return t.text
        except Exception:
            pass
        return el.text

    def get_current_temperature(self) -> str:
        el = self.find(*self.LOC_CURRENT_TEMP)
        return el.get_attribute("content-desc")

    def get_current_temp_number(self) -> str:
        el = self.find(*self.LOC_CURRENT_TEMP_TEXT)
        return el.text

    def get_high_low_temp(self) -> str:
        el = self.find(*self.LOC_HIGH_LOW_TEMP)
        return el.get_attribute("content-desc")

    def get_yesterday_compare_text(self) -> str:
        return self.find(*self.LOC_YESTERDAY_COMPARE).text

    def get_weather_status_text(self) -> str:
        return self.find(*self.LOC_WEATHER_STATUS).text

    def is_weather_info_displayed(self) -> bool:
        return self.is_displayed(*self.LOC_WEATHER_INFO_AREA)

    def is_yesterday_compare_displayed(self) -> bool:
        return self.is_displayed(*self.LOC_YESTERDAY_COMPARE)

    def get_life_info_cards(self) -> list[dict]:
        """미세먼지, 바람, 습도, 강수확률 카드 정보를 반환합니다."""
        names = self.finds(*self.LOC_LIFE_INFO_NAME)
        values = self.finds(*self.LOC_LIFE_INFO_VALUE)
        return [{"name": n.text, "value": v.text} for n, v in zip(names, values)]

    def tap_search(self):
        self.find(*self.LOC_SEARCH_BTN).click()

    def tap_menu(self):
        self.find(*self.LOC_MENU_BTN).click()

    def _find_forecast_tab(self, tab_text: str):
        """단기예보 컨테이너 내의 탭을 찾습니다."""
        container = self.find(AppiumBy.ID, f"{PKG}:id/short_forecast_container")
        tabs = container.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        for tab in tabs:
            if tab.text == tab_text:
                return tab
        raise Exception(f"단기예보 탭 '{tab_text}'을 찾을 수 없음")

    def tap_forecast_tab_weather(self):
        self._find_forecast_tab("날씨").click()

    def tap_forecast_tab_wind(self):
        self._find_forecast_tab("바람").click()

    def tap_forecast_tab_humidity(self):
        self._find_forecast_tab("습도").click()

    def is_forecast_graph_displayed(self) -> bool:
        return self.is_displayed(*self.LOC_FORECAST_GRAPH)
