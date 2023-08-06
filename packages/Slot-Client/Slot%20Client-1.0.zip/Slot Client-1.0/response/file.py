# coding: utf-8

import re

from file_type import FileType
from upload_user import UploadUser

class File(object):

    def __init__(self, jsonObject):
        self._fileSystemId = jsonObject['fileSystemId']
        self._uuid = jsonObject['uuid']
        self._projectId = jsonObject['projectId']
        self._fileName = jsonObject['fileName']
        self._uploadDate = jsonObject['uploadDate']
        self._md5 = jsonObject['md5']
        self._sizeInBytes = jsonObject['sizeInBytes']
        self._mimeType = jsonObject['mimeType']
        self._publicFile = jsonObject['publicFile']
        self._completed = jsonObject['completed']
        self._parentId = jsonObject['parentId']
        self._fileTypes = [FileType(fileTypeJson) for fileTypeJson in jsonObject['fileTypes']]
        if jsonObject['uploadedBy'] is not None:
            self._uploadedBy = UploadUser( jsonObject['uploadedBy'] )
        self._dbLoaded = jsonObject['dbLoaded']
        self._pmFileMetadata = jsonObject['pmFileMetadata']
        self._id = jsonObject['id']

    @property
    def file_system_id(self):
        return self._fileSystemId

    @property
    def uuid(self):
        return self._uuid

    @property
    def project_id(self):
        return self._projectId

    @property
    def file_name(self):
        return self._fileName

    @property
    def upload_date(self):
        return self._uploadDate

    @property
    def md5(self):
        return self._md5

    @property
    def size_in_bytes(self):
        return self._sizeInBytes

    @property
    def public_file(self):
        return self._publicFile

    @property
    def completed(self):
        return self._completed

    @property
    def parent_id(self):
        return self._parentId

    @property
    def file_types(self):
        return self._fileTypes

    @property
    def uploaded_by(self):
        return self._uploadedBy

    @property
    def db_loaded(self):
        return self._dbLoaded

    @property
    def pm_file_metadata(self):
        return self._pmFileMetadata

    @property
    def id(self):
        return self._id