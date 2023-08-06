# coding: utf-8

import re
import json

class UploadFileRequest:

    def __init__(self, id, file_name, extension):
        self.id = id
        self.file_name = file_name
        self.extension = extension

    @property
    def id(self):
        return self.id

    @property
    def file_name(self):
        return self.file_name

    @property
    def extension(self):
        return self.extension

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)