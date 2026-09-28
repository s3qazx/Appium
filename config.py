import os

BASE_DIR = os.path.dirname(__file__)
APPIUM_SEVER = "http://localhost:4723"
DEVICE_CONFIG = {
    "automationName": "UiAutomator2",
    "platformName": "Android",
    "platformVersion": "12",
    "deviceName": "Android Emulator",
    "waitForIdleTimeout": 1000,
    "waitForSelectorTimeout": 0
}
APP_CONFIG = {
    "appPackage": "com.netease.yanxuan",
    "appActivity": ".SplashActivityDefault",
    "noReset": True,
}
First_APP_CONFIG = {
    "appPackage": "com.netease.yanxuan",
    "appActivity": ".SplashActivityDefault",
}