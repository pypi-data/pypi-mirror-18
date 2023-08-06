# -*- coding: utf-8 -*-


import logging
import six
from datetime import datetime


logger = logging.getLogger(__name__)


class MongoField(object):
    _value = None
    _nullable = True
    _default = None
    _mutable = True
    _primary_key = False
    _build_index = False
    _max_length = None
    _updated = False
    _required = False

    def __init__(self, *args, **kwargs):
        for k, v in six.iteritems(kwargs):
            name = '_' + k

            if hasattr(self, name):
                self.__setattr__(name, v)

        if self._value is None:
            self._value = self._default() if callable(self._default) else self._default

    @property
    def updated(self):
        return self._updated

    @updated.setter
    def updated(self, val):
        self._updated = val

    @property
    def mutable(self):
        return self._mutable

    @mutable.setter
    def mutable(self, val):
        self._mutable = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self._value != val:
            self._value = val
            self.updated = True

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, val):
        self._required = val

    def get_value(self):
        return self._value


class StringField(MongoField):
    _default = ''
    _max_length = 1024


class IntegerField(MongoField):
    pass


class FloatField(MongoField):
    pass


class TextField(StringField):
    _max_length = 4096


class DateTimeField(MongoField):
    _default = datetime.now


class ObjectIDField(MongoField):
    pass
