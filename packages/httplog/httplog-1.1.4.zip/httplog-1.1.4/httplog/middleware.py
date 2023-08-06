# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json

from django.conf import settings
from django.utils.functional import SimpleLazyObject
from importlib import import_module

from constance import config

from .decorators import handle_exception
from .services import get_httplog_data, save_httplog_data, get_es_log_data, get_user, \
    get_response_data, save_response_data, get_request_user
from .tasks import task_http_log


class HttpLogExtractMiddleware(object):

    def __init__(self):
        self.engine = import_module(settings.SESSION_ENGINE)

    def __call__(self):
        self.http_log = None
        self.http_log_data = None

    def set_session(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.engine.SessionStore(session_key)
        request.user = SimpleLazyObject(lambda: get_user(request))

    def is_valid_method(self, request):
        return request.method in self.http_log_config.get('METHODS', [])

    def is_valid_url(self, request):
        return request.path in self.http_log_config.get('PERMITTED_URLS', [])

    def is_valid_user(self, request):
        return hasattr(request, 'user') and request.user.id

    def is_valid_config(self):
        return hasattr(settings, 'HTTP_LOG_CONFIG')

    def is_log_to_db(self):
        return self.http_log_config.get('LOG_TO_DB', False)

    def is_log_to_es(self):
        return self.http_log_config.get('LOG_TO_ES', False)

    @handle_exception
    def process_request(self, request):
        self.set_session(request)
        self.http_log_config = json.loads(config.HTTP_LOG_CONFIG)

        if self.is_valid_method(request) and self.is_valid_url(request) and self.is_valid_user(request):
            http_log_data = get_httplog_data(request)
            self.http_log_data = http_log_data

            if self.is_valid_config() and self.is_log_to_db():
                self.http_log = save_httplog_data(self.http_log_data, request)

    @handle_exception
    def process_response(self, request, response):
        if self.is_valid_method(request) and self.is_valid_url(request) and self.is_valid_user(request):
            response_data = get_response_data(response)

            if self.is_valid_config() and self.is_log_to_db() and getattr(self, 'http_log', None):
                save_response_data(self.http_log, response_data)

            if self.is_valid_config() and self.is_log_to_es():
                es_log_data = get_es_log_data(self.http_log_data, response_data, get_request_user(request))
                task_http_log(es_log_data)

        return response
