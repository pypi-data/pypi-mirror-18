# coding: utf-8

import re

class FileType(object):

    def __init__(self, jsonObject):
        self._data_type = jsonObject['dataType']
        self._format = jsonObject['format']
        self._vendor = jsonObject['vendor']
        self._id = jsonObject['id']

    @property
    def data_type(self):
        return self._data_type

    @property
    def format(self):
        return self._format

    @property
    def vendor(self):
        return self._vendor

    @property
    def id(self):
        return self._id