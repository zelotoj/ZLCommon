#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import web

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep

DEFAULT_ROOT_PATH = 'templates/'
DEFAULT_RENDER = web.template.render(DEFAULT_ROOT_PATH, globals={})
DEFAULT_URLS = ('/', 'DoIndex')
DEFAULT_INDEX = '''
<html>
    <head>
        <title>测试</title>
        <meta http-equiv="refresh" content="120">
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style type="text/css"></style>
    </head>
    <body align="center">
    </body>
</html>
'''


class DoIndex:
    def GET(self):
        # raise web.seeother("/")
        return DEFAULT_RENDER.index()


class ZLWebpy(web.application, object):
    """Webpy服务器

    render = web.template.render('templates/', globals={})
    urls = (
        '/', 'do_index',
    )

    class do_index:
        def GET(self):
            userCmd = web.input(index=0)
            # raise web.seeother("/")
            return render.index(links, int(userCmd.index))

    app = WebpyApplication(urls, globals())
    app.run()
    """
    def __init__(self, mapping=None, var=None, auto_reload=None):
        mapping = mapping if mapping else DEFAULT_URLS
        real_root = RUNNING_PATH + DEFAULT_ROOT_PATH
        if not os.path.isdir(real_root):
            os.mkdir(real_root)
        filename_index = real_root + 'index.html'
        if not os.path.isfile(filename_index):
            file(filename_index, 'w').write(DEFAULT_INDEX)
        var = var if var else globals()
        super(ZLWebpy, self).__init__(mapping, var, auto_reload)

    def run(self, port=8080, address='0.0.0.0', *middleware):
        """启动服务器

        :param port: 绑定端口
        :param address: 绑定地址
        :param middleware: 解释器函数
        :return: 无
        """
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (address, port))
