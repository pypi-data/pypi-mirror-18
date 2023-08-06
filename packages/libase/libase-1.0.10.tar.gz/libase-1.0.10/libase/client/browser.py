#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   browser.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import json
import os
import requests

from requests.cookies import (
    RequestsCookieJar,
    )
from requests.structures import (
    CaseInsensitiveDict,
    )
from urlparse import (
    ParseResult,
    urlunparse,
    )

from time import time as get_cur_ts


class SmartJsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, RequestsCookieJar):
            return str(o)
        if isinstance(o, CaseInsensitiveDict):
            return dict(o)
        return super(SmartJsonEncoder, self).default(o)


json_default = SmartJsonEncoder().default


def smart_json_dump(o):
    return json.dumps(o, indent=4, default=json_default)


class PyBrowser(object):

    USER_AGENT = 'Python Browser'

    def __init__(self, user_agent=USER_AGENT, headers=None, cookies=None):
        self.user_agent = user_agent

        self.headers = headers or {}

        self.session = requests.Session()

    def wrap_headers(self, headers=None):
        if not self.headers:
            return headers

        base = self.headers.copy()
        if headers:
            base.update(headers)

        return base

    def request(self, method, url, headers=None, cookies=None, **kwargs):
        headers = self.wrap_headers(headers=headers)

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            cookies=cookies,
            **kwargs
            )

        params = kwargs.get('params')
        data = kwargs.get('json')

        self.show_response(response=response)

        return response

    def show_response(self, response):
        request = response.request
        body = request.body
        body = json.loads(body) if body else None

        print request.method, request.url, response.status_code
        print '>>>'
        print smart_json_dump(request.headers)
        print smart_json_dump(body)
        print '<<<'
        print smart_json_dump(response.headers)
        print smart_json_dump(response.json())

        return response


class PyApiBrowser(PyBrowser):

    HOST = 'localhost'
    PORT = 80
    PREFIX = '/'

    def __init__(self, host=HOST, port=PORT, prefix=PREFIX, **kwargs):
        super(PyApiBrowser, self).__init__(**kwargs)

        self.host = host
        self.port = port
        self.prefix = prefix

    def request(self, method, path, **kwargs):
        assert path[0] == '/'
        netloc = '%s:%d' % (self.host, self.port)
        path = os.path.join(self.prefix, path[1:])

        url = urlunparse(ParseResult(
            'http',
            netloc,
            path,
            '',
            '',
            '',
            ))

        return super(PyApiBrowser, self).request(
            method=method,
            url=url,
            **kwargs
            )

    def post(self, path, **kwargs):
        return self.request(
            method='POST',
            path=path,
            **kwargs
            )

    def delete(self, path, **kwargs):
        return self.request(
            method='DELETE',
            path=path,
            **kwargs
            )

    def put(self, path, **kwargs):
        return self.request(
            method='PUT',
            path=path,
            **kwargs
            )

    def get(self, path, **kwargs):
        return self.request(
            method='GET',
            path=path,
            **kwargs
            )

    def surf_one(self, method, url, kwargs=None, comment=None, expect_code=200,
            expected_data=None, testers=()):
        if comment:
            print '#' * 3, comment

        method = getattr(self, method, None)
        if not method:
            return

        if not kwargs:
            kwargs = {}

        response = method(url, **kwargs)

        if expect_code and response.status_code != expect_code:
            print '!' * 3, 'Bad Code', '%d != %d' % (response.status_code, expect_code)


    def surf(self, *configs):
        for config in configs:
            self.surf_one(**config)
            print


HOST, PORT = 'bar.icampus.us', 80
#HOST, PORT = 'localhost', 5000

browser = PyApiBrowser(host=HOST, port=PORT, prefix='/api/v1')

browser.surf(
    dict(
        comment='注册',
        method='post',
        url='/user',
        kwargs=dict(
            json={
                'account': {
                    'email': '11@11.com',
                    'password': '111',
                    },
                },
            ),
        expect_code=200,
        ),

    dict(
        comment='注册后未登录不能获取当前用户信息',
        method='get',
        url='/user/000000000000000000000000',
        kwargs=dict(),
        expect_code=401,
        ),

    dict(
        comment='登录',
        method='post',
        url='/user/auth',
        kwargs=dict(
            json={
                'ident': '11@11.com',
                'password': '111',
                },
            ),
        expect_code=200,
        ),

    dict(
        comment='获取当前用户信息',
        method='get',
        url='/user/000000000000000000000000',
        kwargs=dict(),
        expect_code=401,
        ),

    dict(
        comment='注销登录',
        method='delete',
        url='/user/auth',
        kwargs=dict(),
        expect_code=200,
        ),

    dict(
        comment='登录',
        method='post',
        url='/user/auth',
        kwargs=dict(
            json={
                'ident': '11@11.com',
                'password': '111',
                },
            ),
        expect_code=200,
        ),

    dict(
        comment='注销账号',
        method='delete',
        url='/user/000000000000000000000000',
        kwargs=dict(),
        expect_code=200,
        ),

    dict(
        comment='',
        method='',
        url='',
        kwargs=dict(),
        expect_code=200,
        ),
    )

raise

print '### 获取用户信息(自己)'
browser.get(
    '/user/000000000000000000000000',
    )

print '### 登录'
browser.post(
    '/user/auth',
    json=data,
    )

print '### 注销账号'
browser.delete(
    '/user/000000000000000000000000',
    )

print '未登录不能获取用户信息(自己)'
browser.get(
    '/user/000000000000000000000000',
    )
