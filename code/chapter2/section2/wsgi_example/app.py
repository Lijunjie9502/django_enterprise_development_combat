# -*- coding:utf-8 -*-
###
# Author: Li Junjie
# Date: 2020-04-29 21:21:25
# LastEditors: Li Junjie
# LastEditTime: 2020-04-29 21:23:31
# FilePath: \django_enterprise_development_combat\code\chapter2\section2\wsgi_example\app.py
###


def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world! -by the5fire \n']