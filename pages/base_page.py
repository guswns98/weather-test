from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def finds(self, by, value):
        return self.wait.until(EC.presence_of_all_elements_located((by, value)))

    def find_by_id(self, resource_id: str):
        return self.find(AppiumBy.ID, resource_id)

    def find_by_text(self, text: str):
        return self.find(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')

    def find_by_text_contains(self, text: str):
        return self.find(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")')

    def is_displayed(self, by, value, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except Exception:
            return False

    def scroll_down(self):
        size = self.driver.get_window_size()
        self.driver.swipe(
            size["width"] // 2,
            int(size["height"] * 0.7),
            size["width"] // 2,
            int(size["height"] * 0.3),
            duration=800,
        )

    def scroll_up(self):
        size = self.driver.get_window_size()
        self.driver.swipe(
            size["width"] // 2,
            int(size["height"] * 0.3),
            size["width"] // 2,
            int(size["height"] * 0.7),
            duration=800,
        )

    def swipe_left(self):
        size = self.driver.get_window_size()
        self.driver.swipe(
            int(size["width"] * 0.8),
            size["height"] // 2,
            int(size["width"] * 0.2),
            size["height"] // 2,
            duration=800,
        )
