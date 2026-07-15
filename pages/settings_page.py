from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

PKG = "weather.forecast.rain.radar"


class SettingsPage(BasePage):
    """설정(메뉴) 화면 Page Object.

    메뉴 진입 후 Appium Inspector로 locator 확인 필요.
    """

    LOC_BACK_BTN = (AppiumBy.ACCESSIBILITY_ID, "뒤로 가기")

    def tap_back(self):
        self.find(*self.LOC_BACK_BTN).click()
