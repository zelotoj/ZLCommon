#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep

DEFAULT_ADDRESS = '0.0.0.0'
DEFAULT_PORT = 8080
DEFAULT_PATH = [('/', RUNNING_PATH + 'www')]


class RequestHandler(SimpleHTTPRequestHandler):
    path_mappings = None

    def translate_path(self, path):
        root = os.getcwd()
        # look up routes and get root directory
        for patt, rootDir in self.path_mappings:
            if path.startswith(patt):
                path = path[len(patt):]
                root = rootDir
            break
        # new path
        result = os.path.join(root, path)
        print result
        return result


class ZLWebServer(object):
    """Web服务器

    """
    def __init__(self, port=DEFAULT_PORT, address=DEFAULT_ADDRESS, path_mappings=None):
        """初始化

        :param port: 绑定端口
        :param address: 绑定地址
        :param path_mappings: 路径映射
        :return: 无
        """
        request_handler = RequestHandler
        request_handler.path_mappings = path_mappings if path_mappings else DEFAULT_PATH
        for (www_path, real_path) in request_handler.path_mappings:
            if not os.path.isdir(real_path):
                os.mkdir(real_path)
        server_class = BaseHTTPServer.HTTPServer
        server_protocol = "HTTP/1.0"
        server_address = (address, port)
        request_handler.protocol_version = server_protocol
        print server_address
        self.httpd = server_class(server_address, request_handler)

    def start(self):
        sa = self.httpd.socket.getsockname()
        print "Serving HTTP http://%s:%d/" % (sa[0], sa[1])
        self.httpd.serve_forever()
