#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import os
import Queue
import ZLThread
import ZLNetworkTools

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class ZLScannerItem(object):
    """扫描项
    
    """

    def __init__(self, ip=None, state=False):
        """初始化
        
        :param ip: IP地址
        :param state: 状态
        :return: 无
        """
        self.ip = ip
        self.port = None
        self.is_tcp = True
        self.state = state


class ZLScanner(object):
    """扫描器
    
    onScanStart 扫描开始回调函数，默认为None
    onScanComplete 扫描完成回调函数，默认为None
    scan_method 扫描方法，默认Ping（methodPing）
    thread_max 扫描线程数量，默认为4个
    retry_max 扫描重试次数，默认为2次
    """
    def __init__(self, retry_max=2, thread_max=4, scan_method=ZLNetworkTools.ZLNetworkTools.ping):
        """初始化

        :param retry_max: 扫描重试次数，默认为2次
        :param thread_max: 扫描线程数量，默认为4个
        :param scan_method: 扫描方法，默认Ping（methodPing）
        :return: 无
        """
        self.retry_max = retry_max
        self.thread_max = thread_max
        self.scan_method = scan_method if scan_method else ZLNetworkTools.ZLNetworkTools.ping
        self.__queuePing = Queue.Queue()

    def on_start(self, items):
        pass

    def on_item_start(self, item):
        pass

    def on_item_complete(self, item):
        pass

    def on_complete(self, items):
        pass

    def start(self):
        """开始扫描

        :return: 无
        """
        self.__mainThread = ZLThread.ZLThread(self.__worker_main)
        self.__mainThread.start()

    def wait(self):
        """等待扫描完成

        :return: 无
        """
        if self.__mainThread.isAlive():
            self.__mainThread.join()

    def __worker_main(self):
        items = list()
        self.on_start(items)
        for item in items:
            if not isinstance(item, ZLScannerItem):
                raise TypeError('items must be ScannerItem list')
            self.__queuePing.put(item)
        for i in xrange(self.thread_max):
            scan_thread = ZLThread.ZLThread(self.__worker_scan)
            scan_thread.start()
        if len(items) > 0:
            self.__queuePing.join()
        self.on_complete(items)

    def __worker_scan(self):
        while not self.__queuePing.empty():
            item = self.__queuePing.get()
            if isinstance(item, ZLScannerItem):
                self.on_item_start(item)
                if item.port:
                    item.state = self.scan_method(item.ip, item.port, item.is_tcp, self.retry_max)
                else:
                    item.state = self.scan_method(item.ip, self.retry_max)
                self.on_item_complete(item)
            self.__queuePing.task_done()
