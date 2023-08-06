# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import re

from django.conf import settings
from django.utils.functional import SimpleLazyObject
from importlib import import_module

from constance import config

from .decorators import handle_exception
from .services import is_valid_config, is_valid_method, is_valid_user, \
    get_httplog_config, get_httplog_data, get_user
from .tasks import task_http_log


class HttpLogExtractMiddleware(object):

    def __init__(self):
        self.engine = import_module(settings.SESSION_ENGINE)
        self.request_body = None
        self.http_log_config = None
        self.permitted_url = None

    def __call__(self):
        self.request_body = None
        self.http_log_config = None
        self.permitted_url = None

    def set_session(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.engine.SessionStore(session_key)
        request.user = SimpleLazyObject(lambda: get_user(request))

    def is_valid_url(self, request):
        permitted_urls = self.http_log_config.get('PERMITTED_URLS', [])
        for permitted_url in permitted_urls:
            if re.match(permitted_url, request.path):
                self.permitted_url = permitted_url
                return True
        return False

    @handle_exception
    def process_request(self, request):
        self.set_session(request)
        self.http_log_config = get_httplog_config()
        self.request_body = request.body

    @handle_exception
    def process_response(self, request, response):
        if is_valid_method(request, self.http_log_config) and self.is_valid_url(request) and is_valid_user(request):
            http_log_data = get_httplog_data(request, self.request_body, response, getattr(self, 'permitted_url', None))

            if is_valid_config():
                task_http_log(self.http_log_config, http_log_data, request)

        return response
