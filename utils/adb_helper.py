"""adb 명령어 기반 유틸리티 - 잠금 화면 등 Appium 세션 밖 영역 검증용."""
import subprocess
import time
import xml.etree.ElementTree as ET


def run_adb(args: list[str]) -> str:
    """adb 명령어를 실행하고 stdout을 반환합니다."""
    result = subprocess.run(
        ["adb"] + args,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def is_screen_on() -> bool:
    """디스플레이가 켜져 있는지 확인합니다."""
    output = run_adb(["shell", "dumpsys", "power"])
    return "mWakefulness=Awake" in output


def turn_screen_off():
    """디스플레이를 끕니다."""
    if is_screen_on():
        run_adb(["shell", "input", "keyevent", "KEYCODE_POWER"])
        time.sleep(1)


def turn_screen_on():
    """디스플레이를 켭니다 (잠금 해제 없이)."""
    if not is_screen_on():
        run_adb(["shell", "input", "keyevent", "KEYCODE_WAKEUP"])
        time.sleep(2)


def dump_ui() -> ET.Element:
    """현재 화면의 UI 트리를 덤프하여 XML Element로 반환합니다."""
    run_adb(["shell", "uiautomator", "dump", "/sdcard/ui_dump.xml"])
    xml_output = run_adb(["shell", "cat", "/sdcard/ui_dump.xml"])
    return ET.fromstring(xml_output)


def find_elements_by_resource_id(root: ET.Element, resource_id: str) -> list[ET.Element]:
    """resource-id로 요소를 검색합니다."""
    full_id = f"weather.forecast.rain.radar:id/{resource_id}"
    return [node for node in root.iter("node") if node.get("resource-id") == full_id]


def take_screenshot(save_path: str):
    """adb로 스크린샷을 캡처합니다."""
    run_adb(["shell", "screencap", "-p", "/sdcard/screenshot.png"])
    run_adb(["pull", "/sdcard/screenshot.png", save_path])
