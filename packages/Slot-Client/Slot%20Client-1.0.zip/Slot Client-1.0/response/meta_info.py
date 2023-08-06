# coding: utf-8
import re
import json

class MetaInfo(object):

    def __init__(self, jsonObject):
        self._tables = json.dumps([table for table in jsonObject['tables']])

    @property
    def tables(self):
        return self._tables