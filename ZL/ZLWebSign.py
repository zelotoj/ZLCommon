#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import urlparse
import ZLWebSign_indmi
import ZLWebSign_zimuzu

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class ZLWebSign(object):
    def __init__(self):
        super(ZLWebSign, self).__init__()
        self.sign_types = dict()
        self.add_sign_type(ZLWebSign_indmi.ZLWebSign_indmi)
        self.add_sign_type(ZLWebSign_zimuzu.ZLWebSign_zimuzu)

    def start(self, url, username, password):
        user_hostname = ZLWebSign.get_hostname(url)
        if self.sign_types.has_key(user_hostname):
            web_sign = self.sign_types[user_hostname](url, username, password)
            web_sign.start()

    @staticmethod
    def get_hostname(url):
        return urlparse.urlparse(url).hostname if url else None

    def add_sign_type(self, type):
        self.sign_types[ZLWebSign.get_hostname(type.url_host)] = type
