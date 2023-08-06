# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .base import DynamicFieldsModelSerializer, UserField

from .models.httplog import HttpLog


class HttpLogSerializer(DynamicFieldsModelSerializer):
    user = UserField()

    class Meta:
        model = HttpLog
