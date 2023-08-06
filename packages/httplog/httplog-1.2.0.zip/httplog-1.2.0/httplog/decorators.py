# -*- coding: utf-8 -*-
from __future__ import absolute_import
from functools import wraps
import json

from .services import is_valid_config, get_httplog_data, get_httplog_config

from .tasks import task_http_log


def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            if func.__name__ == 'process_response':
                return args[2]
    return wrapper


def httplog_handler(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):

        queryset = func(*args, **kwargs)

        request = args[1]

        if request.data.has_key('operator'):
            request.data.pop('operator')

        if is_valid_config():
            http_log_data = get_httplog_data(request, request.data, queryset)
            http_log_config = get_httplog_config()
            task_http_log(http_log_config, http_log_data, request)

        return queryset

    return func_wrapper
