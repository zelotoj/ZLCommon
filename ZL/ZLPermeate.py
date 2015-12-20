#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import datetime

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class ZLPermeate(object):
    commands = {
        'uptime': 'cat /proc/uptime',
        'loadavg': 'cat /proc/loadavg',
        'meminfo': 'cat /proc/meminfo',
        'cpuinfo': 'cat /proc/cpuinfo',
    }

    @classmethod
    def local(cls):
        pass

    @classmethod
    def ssh(cls):
        pass

    @classmethod
    def permeate(cls):
        pass

    @staticmethod
    def decode_loadavg(loadavg_string):
        result = dict()
        if loadavg_string:
            cpu_values = str(loadavg_string).split()
            result['CPU_1'] = float(cpu_values[0])
            result['CPU_5'] = float(cpu_values[1])
            result['CPU_15'] = float(cpu_values[2])
            result['last_pid'] = cpu_values[4]
        return result

    @staticmethod
    def decode_uptime(uptime_string):
        result = dict()
        if uptime_string:
            uptime_values = str(uptime_string).split()
            all_sec = float(uptime_values[0])
            minute, hour, day = 60, 3600, 86400
            up_time = datetime.timedelta(
                days=int(all_sec / day),
                hours=int((all_sec % day) / hour),
                minutes=int((all_sec % hour) / minute),
                seconds=int(all_sec % minute)
            )
            result['uptime'] = up_time
            result['freerate'] = (float(uptime_values[1]) / float(uptime_values[0]))
        return result

    @staticmethod
    def decode_meminfo(meminfo_string):
        result = dict()
        if meminfo_string:
            lines = str(meminfo_string).split(os.linesep)
            for line in lines:
                if len(line) < 2: continue
                name = line.split(':')[0]
                var = line.split(':')[1].split()[0]
                result[name] = long(var) * 1024.0
            result['MemUsed'] = result['MemTotal'] - result['MemFree'] - result['Buffers'] - result['Cached']
        return result

    @staticmethod
    def decode_cpuinfo(cpuinfo_string):
        result = dict()
        if cpuinfo_string:
            pass
        return result
