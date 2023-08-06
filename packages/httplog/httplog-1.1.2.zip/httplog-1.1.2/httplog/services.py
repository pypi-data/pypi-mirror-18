# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import decisionTable
from constance import config
from django.forms import model_to_dict
from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings
from .serializers import HttpLogSerializer
from rest_framework.response import Response


def get_request_ip(request):
    if request.META is 'HTTP_X_FORWARDED_FOR':
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']


def get_client_data(request):
    return {
        'ip': get_request_ip(request),
    }


def get_server_data(request):
    server = request.META['HTTP_HOST'].split(':')

    return {
        'host': server[0],
        'port': server[1],
    }


def get_request_data(request):
    return {
        'method': request.method,
        'path': request.path,
        'data': json.loads(request.body),
    }


def get_request_user(request):
    return User.objects.get(id=request.user.id)


def get_httplog_name(request):
    table = decisionTable.DecisionTable(config.HTTP_LOG_CONFIG_DECISION_TABLE)
    return table.decision(['name'], url=request.path, method=request.method)


def get_httplog_data(request):
    return {
        'name': get_httplog_name(request),
        'client': get_client_data(request),
        'server': get_server_data(request),
        'request': get_request_data(request)
    }


def save_httplog_data(request_data, request):
    serializer = HttpLogSerializer(data=request_data, partial=True)

    if serializer.is_valid():
        user = get_request_user(request)
        return serializer.save(user=user)


def get_response_data(response):
    if isinstance(response, Response):
        return {
            'status_code': response.status_code,
            'data': response.data,
        }
    else:
        return {}


def save_response_data(http_log, response_data):
    http_log.response = response_data
    http_log.save(update_fields=['response'])


def get_es_log_data(http_log_data, response_data, user):
    http_log_data['response'] = response_data
    http_log_data['user'] = model_to_dict(user)
    return http_log_data


def get_hostname():
    return settings.REST_CLIENT_SETTINGS['ES']['default']['HOSTNAME']


def get_port():
    return settings.REST_CLIENT_SETTINGS['ES']['default']['PORT']


def set_es_url():
    return '{}:{}'.format(get_hostname(), get_port())


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user
