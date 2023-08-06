# coding: utf-8
import re
from project_operator import ProjectOperator

class Project(object):

    def __init__(self, jsonObject):
        self._id = jsonObject['id']
        self._name = jsonObject['name']
        self._username = jsonObject['username']
        self._description = jsonObject['description']
        if jsonObject['operator'] is not None:
            self._operator = ProjectOperator(jsonObject['operator'])
        self._creationDate = jsonObject['creationDate']
        self._klondikeId = jsonObject['klondikeId']
        self._flavour = jsonObject['flavour']

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def username(self):
        return self._username

    @property
    def description(self):
        return self._description

    @property
    def operator(self):
        return self._operator

    @property
    def creation_date(self):
        return self._creationDate

    @property
    def klondike_id(self):
        return self._klondikeId

    @property
    def flavour(self):
        return self._flavour