#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import threading

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class ZLThread(threading.Thread):
    """线程类

    """
    def __init__(self, func, error_callback=None):
        """初始化

        :param func: 调用函数
        :param error_callback: 错误回调函数
        :return: 无
        """
        super(ZLThread, self).__init__()
        self.daemon = True
        self.__Func = func
        self.__ErrorCallback = error_callback

    def run(self):
        """线程运行函数

        :return: 无
        """
        try:
            self.__Func()
        except Exception, e:
            if self.__ErrorCallback:
                self.__ErrorCallback(e)
            else:
                raise e
        finally:
            return
