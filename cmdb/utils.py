#!/usr/bin/env python
#coding:utf8

import re
from rest_framework.views import exception_handler

r = re.compile(r'[\.]+')

def validIPV4(s):      
    ip_list = r.split(s)
    if len(ip_list) != 4:
        print('IP地址格式不正确')
        return False
    for i in ip_list:
        if i.isdigit():
            if int(i) not in xrange(0, 256):
                print('IP地址不合法')
                return False
        else:
            print('IP地址不合法, 含非数字')
            return False
    return True

def customExceptionHandler(exception, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exception, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
    return response