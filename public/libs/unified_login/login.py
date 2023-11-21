import logging

from public.base.basics import Base
# from libs.common.read_config import ini
from public.libs.unified_login.page_object.login import *

from time import sleep
from selenium import webdriver

class Login(Base):
    """登录类"""
    def feishu_login(self, drivers, url, username, passwd):
        """统一登录֤"""
        user = LoginPage(drivers)
        user.get_url(url) # 跳转到指定网页
        user.fs_click_close()
        user.fs_click_HomeLogin()
        user.fs_click_account()
        user.fs_input_account(username) # 输入帐户名
        user.fs_input_agreement()
        user.fs_input_passwd(passwd) # 输入密码
        user.fs_click_login()
        sleep(3)


