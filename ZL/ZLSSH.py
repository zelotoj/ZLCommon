#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import datetime
import re
import paramiko

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class ZLSSH_Item(object):
    def __init__(self, host, port, username=None, password=None, key_filename=None, timeout=5):
        super(ZLSSH_Item, self).__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.timeout = timeout


class ZLSSH(object):
    def __init__(self, host, port, username=None, password=None, key_filename=None, timeout=5):
        super(ZLSSH, self).__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.timeout = timeout
        self.__client = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        self.close()
        self.__client = paramiko.SSHClient()
        self.__client.load_system_host_keys()
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.key_filename:
            key = paramiko.RSAKey.from_private_key_file(self.key_filename, self.password)
            self.__client.connect(self.host, self.port, self.username, pkey=key, timeout=self.timeout)
        else:
            self.__client.connect(self.host, self.port, self.username, self.password, timeout=self.timeout)

    def exec_command(self, command):
        stdin, stdout, stderr = self.__client.exec_command(command)
        result = stdout.read()
        return result

    def close(self):
        if hasattr(self, '__client') and self.__client:
            self.__client.close()
            self.__client = None

    @staticmethod
    def poweroff(host, port, username='root', password=None, key_filename=None):
        cmd = 'poweroff'
        ssh = ZLSSH(host, port, username, password, key_filename)
        ssh.connect()
        cpu_value = ssh.exec_command(cmd)
        ssh.close()

    @staticmethod
    def loadavg(host, port, username='root', password=None, key_filename=None):
        result = None
        cmd = 'cat /proc/loadavg'
        ssh = ZLSSH(host, port, username, password, key_filename)
        ssh.connect()
        cpu_value = ssh.exec_command(cmd)
        ssh.close()
        if cpu_value:
            cpu_values = str(cpu_value).split()
            result = (float(cpu_values[0]), float(cpu_values[1]), float(cpu_values[2]))
        return result

    @staticmethod
    def uptime(host, port, username='root', password=None, key_filename=None):
        result = None
        cmd = 'cat /proc/uptime'
        ssh = ZLSSH(host, port, username, password, key_filename)
        ssh.connect()
        cpu_value = ssh.exec_command(cmd)
        ssh.close()
        if cpu_value:
            cpu_values = str(cpu_value).split()
            all_sec = float(cpu_values[0])
            MINUTE,HOUR,DAY = 60,3600,86400
            up_time = datetime.timedelta(
                days=int(all_sec / DAY),
                hours=int((all_sec % DAY) / HOUR),
                minutes=int((all_sec % HOUR) / MINUTE),
                seconds=int(all_sec % MINUTE)
            )
            result = (up_time, float(cpu_values[1]) / float(cpu_values[0]))
        return result

    @staticmethod
    def get_state(host, port, username='root', password=None, key_filename=None):
        result = dict()
        ssh = ZLSSH(host, port, username, password, key_filename)
        ssh.connect()
        uptime_value = ssh.exec_command('cat /proc/uptime')
        if uptime_value:
            uptime_values = str(uptime_value).split()
            all_sec = float(uptime_values[0])
            MINUTE,HOUR,DAY = 60,3600,86400
            up_time = datetime.timedelta(
                days=int(all_sec / DAY),
                hours=int((all_sec % DAY) / HOUR),
                minutes=int((all_sec % HOUR) / MINUTE),
                seconds=int(all_sec % MINUTE)
            )
            result['uptime'] = up_time
            result['freerate'] = (float(uptime_values[1]) / float(uptime_values[0]))
        ssh.close()
        return result
