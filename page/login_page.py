from selenium.webdriver.common.by import By

from base.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self,app_driver):
        super().__init__(app_driver)
        self.login_loc = By.XPATH,'//android.widget.TabWidget[@resource-id="android:id/tabs"]/android.view.ViewGroup[5]'
        self.change_mode_loc = By.ID, 'com.netease.yanxuan:id/btn_change_mode'
        self.agree_loc =By.ID,'com.netease.yanxuan:id/check_box'
        self.input_user_loc = By.ID, 'com.netease.yanxuan:id/account_edit'
        self.input_passwd_loc = By.ID, 'com.netease.yanxuan:id/password_edit'
        self.login_button_loc = By.XPATH, '//android.widget.LinearLayout[@resource-id="com.netease.yanxuan:id/fl_loginview"]'
        self.login_success_loc = By.ID,'com.netease.yanxuan:id/user_name'
        self.login_fail_loc = By.XPATH,'//android.widget.Toast'

    def before_login(self):
        self.base_click(self.login_loc)
        self.base_click(self.change_mode_loc)
        self.base_click(self.agree_loc)

    def login(self,username,password):
        self.base_input_text(self.input_user_loc,username)
        self.base_input_text(self.input_passwd_loc,password)
        self.base_click(self.login_button_loc)
