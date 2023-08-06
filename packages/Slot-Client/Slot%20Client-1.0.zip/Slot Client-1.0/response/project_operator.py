# coding: utf-8

import re

class ProjectOperator(object):

    def __init__(self, jsonObject):
        self._id = jsonObject['id']
        self._name = jsonObject['name']
        self._country = jsonObject['country']


    @property
    def operator_id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def country(self):
        return self._country

