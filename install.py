#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


def make_path_file():
    packages_path = '/usr/lib/python2.7/dist-packages' + os.sep
    print 'check path: %s' % packages_path
    if os.path.isdir(packages_path):
        path_filename = packages_path + 'ZLCommon.pth'
        if os.path.isfile(path_filename):
            os.remove(path_filename)
        print 'write file: %s' % path_filename
        file(path_filename, 'w').write(SCRIPT_PATH + os.linesep)


def main():
    make_path_file()

if __name__ == '__main__':
    print 'check root ...'
    if os.geteuid():
        print 'input root password.'
        args = [sys.executable] + sys.argv
        # 下面两种写法，一种使用su，一种使用sudo，都可以
        os.execlp('su', 'su', '-c', ' '.join(args))
        # os.execlp('sudo', 'sudo', *args)
    main()
