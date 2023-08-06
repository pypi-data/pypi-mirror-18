# -*- coding: utf-8 -*-

from kkconst import BaseConst, ConstIntField


class BaseStatusCode(BaseConst):
    class Meta:
        allow_duplicated_value = False


class StatusCodeField(ConstIntField):
    def __init__(self, status_code, message='', description=''):
        ConstIntField.__init__(status_code, verbose_name=message, description=description)
        self.message = message
