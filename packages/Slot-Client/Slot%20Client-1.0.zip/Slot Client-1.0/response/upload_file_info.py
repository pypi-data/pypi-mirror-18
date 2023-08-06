# coding: utf-8

import re
from file import File

class UploadFileInfo(object):

    def __init__(self, jsonObject):
        self._task_id = jsonObject['taskId']
        self._file_info = File( jsonObject['fileInfo'] )
        self._message = jsonObject['message']
        self._uploaded = jsonObject['uploaded']
        

    @property
    def task_id(self):
        return self._task_id

    @property
    def file_info(self):
        return self._file_info

    @property
    def message(self):
        return self._message

    @property
    def uploaded(self):
        return self._uploaded