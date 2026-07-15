import json
from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def create_android_driver(appium_url: str = "http://127.0.0.1:4723") -> webdriver.Remote:
    caps_path = CONFIG_DIR / "android_caps.json"
    with open(caps_path) as f:
        caps = json.load(f)

    options = UiAutomator2Options().load_capabilities(caps)
    driver = webdriver.Remote(appium_url, options=options)
    driver.implicitly_wait(10)
    return driver
