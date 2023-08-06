# coding: utf-8
import re
import json

class CmInfo(object):

    def __init__(self, jsonObject):
    	self._dataCount = jsonObject['dataCount']
        if jsonObject['dumpDates'] is not None:
    	   self._dumpDates = json.dumps([dumpDateJson for dumpDateJson in jsonObject['dumpDates']])
        if jsonObject['parameterNames'] is not None:
    	   self._parameterNames = json.dumps([parameterName for parameterName in jsonObject['parameterNames']])
        if jsonObject['objectClasses'] is not None:
    	   self._objectClasses = json.dumps([objectClass for objectClass in jsonObject['objectClasses']])

    @property
    def data_count(self):
        return self._dataCount

    @property
    def dump_dates(self):
        return self._dumpDates

    @property
    def parameter_names(self):
        return self._parameterNames

    @property
    def object_classes(self):
        return self._objectClasses