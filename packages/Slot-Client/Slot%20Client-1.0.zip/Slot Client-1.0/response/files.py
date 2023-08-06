# coding: utf-8

import re
from file import File

class Files(object):

    def __init__(self, jsonObject):
    	self._files = [File(fileJson) for fileJson in jsonObject['files']]

    @property
    def files(self):
        return self._files