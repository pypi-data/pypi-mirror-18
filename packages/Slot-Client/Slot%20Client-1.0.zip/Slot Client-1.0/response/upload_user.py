# coding: utf-8

import re

class UploadUser(object):

    def __init__(self, jsonObject):
        self._username = jsonObject['username']
        self._display_name = jsonObject['displayName']
        self._mail = jsonObject['mail']
        self._user_role = jsonObject['userRole']
        self._last_activity = jsonObject['lastActivity']
        self._employee_number = jsonObject['employeeNumber']

    @property
    def username(self):
        return self._username

    @property
    def display_name(self):
        return self._display_name

    @property
    def mail(self):
        return self._mail

    @property
    def user_role(self):
        return self._user_role

    @property
    def last_activity(self):
        return self._last_activity

    @property
    def employee_number(self):
        return self._employee_number