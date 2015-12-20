#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import urlparse
import ZLWebSignBase

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class ZLWebSign_indmi(ZLWebSignBase.ZLWebSignBase):
    url_host = 'http://www.indmi.com/u.php'

    def __init__(self, url, username, password, browser=None, temp_path='/tmp'):
        self.text_no_login = '您没有登录'
        self.text_no_sign = '每日打卡'
        self.text_has_sign = '天打卡'
        super(ZLWebSign_indmi, self).__init__(url, username, password, browser, temp_path)

    def get_text_username(self, browser):
        return browser.find_by_name('pwuser')

    def get_text_password(self, browser):
        return browser.find_by_name('pwpwd')

    def get_button_login(self, browser):
        return browser.find_by_text('登录')

    def get_button_sign(self, browser):
        return browser.find_by_id('punch')



