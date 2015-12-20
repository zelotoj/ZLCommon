#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import time
import datetime
import urlparse
from splinter import Browser

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep
#####################################################
# global instance
CLOASE_AFTER_TEST = False
GBK = "gbk"
UTF8 = "utf8"
#####################################################
# encoding for console
reload(sys)
sys.setdefaultencoding(UTF8)
#####################################################
# small method
encoding = lambda x:x.encode(GBK)
#####################################################


def output(x):
    """
        encode and print
    """
    print encoding(x)


class ZLWebSignBase(object):
    url_host = 'http://www.baidu.com'
    text_no_login = '未登录'
    text_no_sign = '点击签到'
    text_has_sign = '已签到'

    def __init__(self, url, username, password, browser=None, temp_path='/tmp'):
        super(ZLWebSignBase, self).__init__()
        self.url_user = url
        self.username = username
        self.password = password
        self.browser = browser
        self.url_hostname = urlparse.urlparse(self.url_host).hostname
        self.temp_path = temp_path if temp_path[:-1] == os.sep else temp_path + os.sep
        self.url_hostname = urlparse.urlparse(self.url_host).hostname
        self.url_filename = self.temp_path + self.url_hostname
        self.__waittime = 15

    def get_text_username(self, browser):
        return browser.find_by_name('username')

    def get_text_password(self, browser):
        return browser.find_by_name('password')

    def get_button_login(self, browser):
        return browser.find_by_id('login')

    def get_button_sign(self, browser):
        return browser.find_by_id('punch')

    def check_login_state(self, browser):
        result = False
        try:
            if browser.is_text_present(self.text_no_login):
                print '用户 %s 正在登录' % self.username
                self.get_text_username(browser).fill(self.username.decode(UTF8))
                self.get_text_password(browser).fill(self.password.decode(UTF8))
                self.get_button_login(browser).click()
                result = True
        except Exception, ex:
            print ex
        finally:
            return result

    def check_sign_state(self, browser):
        result = False
        try:
            if browser.is_text_present(self.text_no_sign):
                print '用户 %s 正在签到' % self.username
                self.get_button_sign(browser).click()
            elif browser.is_text_present(self.text_has_sign):
                print '用户 %s 签到成功' % self.username
                result = True
        except Exception, ex:
            print ex
        finally:
            return result

    @staticmethod
    def check_date(sign_time):
        now_time = datetime.datetime.now()
        result = True if sign_time.date() == now_time.date() else False
        return result

    def start(self):
        if not self.url_hostname == urlparse.urlparse(self.url_user).hostname:
            return
        if self.__check_sign_date():
            print '网站:%s 用户:%s 已经签到了' % (self.url_hostname, self.username)
        else:
            print '网站:%s 用户:%s 开始签到' % (self.url_hostname, self.username)
            if self.browser:
                self.__worker(self.browser)
            else:
                with Browser() as browser:
                    self.__worker(browser)

    def __worker(self, browser):
        has_login = False
        for i in xrange(self.__waittime):
            browser.visit(self.url_host)
            self.check_login_state(browser)
            if self.check_sign_state(browser):
                sign_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                open(self.url_filename, 'w').write(sign_time)
                break
            time.sleep(1)

    def __check_sign_date(self):
        result = False
        if os.path.isfile(self.url_filename):
            file_string = open(self.url_filename, 'r').read()
            sign_time = datetime.datetime.strptime(file_string, '%Y-%m-%d %H:%M:%S')
            if self.check_date(sign_time):
                result = True
        return result
