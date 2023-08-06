# coding: utf-8
import re

from project import Project
from pm_info import PmInfo
from cm_info import CmInfo
from meta_info import MetaInfo

class Details(object):

    def __init__(self, jsonObject):
        self._project = Project( jsonObject['project'] )
        self._pmInfo = PmInfo( jsonObject['pmInfo'] )
        self._cmInfo = CmInfo( jsonObject['cmInfo'] )
        self._metaInfo = MetaInfo( jsonObject['metaInfo'] )

    @property
    def project(self):
        return self._project

    @property
    def pm_info(self):
        return self._pmInfo

    @property
    def cm_info(self):
        return self._cmInfo

    @property
    def meta_info(self):
        return self._metaInfo