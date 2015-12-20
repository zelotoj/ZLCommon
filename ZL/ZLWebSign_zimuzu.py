#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import urlparse
import ZLWebSignBase

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class ZLWebSign_zimuzu(ZLWebSignBase.ZLWebSignBase):
    url_host = 'http://www.zimuzu.tv/user/sign'

    def __init__(self, url, username, password, browser=None, temp_path='/tmp'):
        self.text_no_login = '登入網站'
        self.text_no_sign = '点击簽到'
        self.text_has_sign = '您今天已簽到'
        super(ZLWebSign_zimuzu, self).__init__(url, username, password, browser, temp_path)

    def get_text_username(self, browser):
        return browser.find_by_name('email')

    def get_text_password(self, browser):
        return browser.find_by_name('password')

    def get_button_login(self, browser):
        return browser.find_by_id('login')

    def get_button_sign(self, browser):
        return browser.find_link_by_text('点击簽到')
