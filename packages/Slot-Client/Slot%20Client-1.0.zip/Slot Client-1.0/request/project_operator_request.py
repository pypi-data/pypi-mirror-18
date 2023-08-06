# coding: utf-8

import re
import json

class ProjectOperatorRequest(object):

    def __init__(self, id):
        self.id = id


    @property
    def operator_id(self):
        return self.id

