# coding: utf-8

import re
import json

from project_operator_request import ProjectOperatorRequest

class CreateProjectRequest:

    def __init__(self, name, username, description, operator_id):
        self.name = name
        self.username = username
        self.description = description
        if operator_id is not None:
            self.operator = ProjectOperatorRequest(operator_id)

    @property
    def name(self):
        return self.name

    @property
    def username(self):
        return self.username

    @property
    def description(self):
        return self.description

    @property
    def operator(self):
        return self.operator

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)