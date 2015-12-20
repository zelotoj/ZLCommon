#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import socket
from enum import IntEnum

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class POWER_VALUE(IntEnum):
    POWER_OFF = 0
    POWER_ON = 1


class HDMI_VALUE(IntEnum):
    HDMI1 = 1
    HDMI2 = 2
    HDMI3 = 3
    DVD = 5


class VOLUME_VALUE(IntEnum):
    VOLUME_10 = 10
    VOLUME_20 = 20
    VOLUME_30 = 30
    VOLUME_40 = 40
    VOLUME_50 = 50


class TIMER_VALUE(IntEnum):
    TIMER_OFF = 0
    TIMER_30 = 1
    TIMER_60 = 2
    TIMER_90 = 3
    TIMER_120 = 4
    TIMER_150 = 5

class ZLSharpTV(object):
    CMD_POWER = 'power'
    CMD_HDMI = 'hdmi'
    CMD_VOLUME = 'volume'
    CMD_SURROUND = 'surround'
    CMD_TIMER = 'timer'
    CMD_WIDE = 'wide'
    STATE_GET = '?'
    STATE_OK = 'OK'
    STATE_ERR = 'ERR'

    def __init__(self, ip, port=10002, timeout=2, debug=False):
        self.__ip = ip
        self.__port = port
        self.__timeout = timeout
        self.__debug = debug
        
        self.__cmd = {
            self.CMD_POWER: 'POWR',
            self.CMD_HDMI: 'IAVD',
            self.CMD_VOLUME: 'VOLM',
            self.CMD_SURROUND: 'ACSU',
            self.CMD_TIMER: 'OFTM',
            self.CMD_WIDE: 'WIDE',
        }

    def send(self, command, value=STATE_GET):
        result = False
        if not command in self.__cmd.keys():
            raise ValueError('command must be ZLSharpTV.CMD_*')
        value = value if isinstance(value, str) else str(value)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.settimeout(self.__timeout)
            client_socket.connect((self.__ip, self.__port))
            send_string = ((self.__cmd[command] + value).ljust(8) + '\r').upper()
            if self.__debug:
                print 'send <%s>' % send_string.replace('\r', '')
            client_socket.send(send_string)
            recv_string = client_socket.recv(9)
            if self.__debug:
                print 'recv <%s>' % recv_string.replace('\r', '')
            recv_string = recv_string.replace('\r', '')
            if recv_string == self.STATE_OK:
                result = True
            elif recv_string == self.STATE_ERR:
                result = False
            elif recv_string.isdigit():
                result = int(recv_string)
        except socket.error, e:
            raise e
        finally:
            client_socket.close()
        if self.__debug:
            print 'ret <%s>' % result
        return result

    def get_power(self):
        return self.send(self.CMD_POWER)

    def set_power(self, power_value):
        return self.send(self.CMD_POWER, power_value)

    def get_hdmi(self):
        return self.send(self.CMD_HDMI)

    def set_hdmi(self, hdmi_number):
        return self.send(self.CMD_HDMI, hdmi_number)

    def get_volume(self):
        return self.send(self.CMD_VOLUME)

    def set_volume(self, volume_value):
        value = volume_value
        if value < 0: value=0
        if value > 100: value=100
        return self.send(self.CMD_VOLUME, value)

    def get_timer(self):
        return self.send(self.CMD_TIMER)

    def set_timer(self, timer_value):
        return self.send(self.CMD_TIMER, timer_value)

    def get_wide(self):
        return self.send(self.CMD_WIDE)

    def set_wide(self, wide_value):
        return self.send(self.CMD_WIDE, wide_value)

    def get_surround(self):
        return self.send(self.CMD_SURROUND)

    def set_surround(self, surround_value):
        return self.send(self.CMD_SURROUND, surround_value)

    def get_state(self):
        result = dict()
        power_state = self.get_power()
        result[self.CMD_POWER] = power_state
        if power_state == POWER_VALUE.POWER_ON:
            result[self.CMD_HDMI] = self.get_hdmi()
            result[self.CMD_VOLUME] = self.get_volume()
        if self.__debug:
            print result
        return result

    def get_all_state(self):
        result = self.get_state()
        if result[self.CMD_POWER] == POWER_VALUE.POWER_ON:
            result[self.CMD_TIMER] = self.get_timer()
            result[self.CMD_WIDE] = self.get_wide()
            result[self.CMD_SURROUND] = self.get_surround()
        if self.__debug:
            print result
        return  result
