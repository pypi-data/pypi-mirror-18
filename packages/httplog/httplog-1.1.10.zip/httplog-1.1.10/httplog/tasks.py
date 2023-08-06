# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from datetime import date
from .services import is_log_to_db, is_log_to_es, save_httplog_data, \
    get_es_log_data, get_request_user, set_es_url

from elasticsearch import Elasticsearch

from celery import shared_task


def datetime_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


@shared_task(serializer='json')
def task_http_log(http_log_config, http_log_data, request):

    if is_log_to_db(http_log_config):
        save_httplog_data(http_log_data, request)

    if is_log_to_es(self.http_log_config):
        es_log_data = get_es_log_data(http_log_data, get_request_user(request))
        body = json.dumps(es_log_data, default=datetime_handler)

        es = Elasticsearch(set_es_url())
        es.index(index='cd_http_log_{}'.format(date.today()),doc_type='log',body=body)
