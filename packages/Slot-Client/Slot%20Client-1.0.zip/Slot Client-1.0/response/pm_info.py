# coding: utf-8
import re
import json

class PmInfo(object):

    def __init__(self, jsonObject):
    	self._dataCount = jsonObject['dataCount']
    	self._dumpDates = json.dumps([dumpDateJson for dumpDateJson in jsonObject['dumpDates']])
    	self._kpiNames = json.dumps([kpiName for kpiName in jsonObject['kpiNames']])
    	self._timeAggregationLevels = json.dumps([timeAggregationLevel for timeAggregationLevel in jsonObject['timeAggregationLevels']])
    	self._objectAggregationLevels = json.dumps([objectAggregationLevel for objectAggregationLevel in jsonObject['objectAggregationLevels']])

    @property
    def data_count(self):
        return self._dataCount

    @property
    def dump_dates(self):
        return self._dumpDates

    @property
    def kpi_names(self):
        return self._kpiNames

    @property
    def time_aggregation_levels(self):
        return self._timeAggregationLevels

    @property
    def object_aggregation_levels(self):
        return self._objectAggregationLevels