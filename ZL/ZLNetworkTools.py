#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import socket
from wakeonlan import wol
import paramiko

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class ZLNetworkTools(object):
    def __init__(self):
        super(ZLNetworkTools, self).__init__()

    @classmethod
    def ping(cls, host, retry=2):
        command = 'ping -c %s %s > /dev/null 2>&1' % (retry, host)
        response = os.system(command)
        result = True if response == 0 else False
        return result

    @classmethod
    def port_test(cls, host, port, is_tcp=True, timeout=2):
        result = False
        socket_type = socket.SOCK_STREAM if is_tcp else socket.SOCK_DGRAM
        client_socket = socket.socket(socket.AF_INET, socket_type)
        try:
            client_socket.settimeout(timeout)
            client_socket.connect((host, port))
            result = True
        except:
            result = False
        finally:
            client_socket.close()
            return result

    @classmethod
    def wakeonlan(cls, mac):
        wol.send_magic_packet(mac)
