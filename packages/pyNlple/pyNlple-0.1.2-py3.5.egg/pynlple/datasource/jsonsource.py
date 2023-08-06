# -*- coding: utf-8 -*-
import io
import json
import requests
from pandas import DataFrame
from pynlple.exceptions import DataSourceException


class JsonDataSource(object):

    @staticmethod
    def dataframe_from_json_array(json_array, keys, fill_na_map=None):
        extracted_entries = list()
        for json_object in json_array:
            entry = dict()
            for key in keys:
                entry[key] = json_object[key]
            extracted_entries.append(entry)
        dataframe = DataFrame(extracted_entries)
        dataframe.set_index('id', inplace=True)
        if fill_na_map:
            for key, value in fill_na_map.items():
                dataframe[key].fillna(value, inplace=True)
        return dataframe


class ServerJsonDataSource(object):
    """Class for providing json data from json files."""

    def __init__(self, url_address, query, authentication=None):
        self.url_address = url_address
        self.query = query
        self.authentication = authentication

    def get_data(self):
        request = requests.post(self.url_address, auth=self.authentication, params=self.query)
        if request.status_code is not 200:
            raise DataSourceException('Could not reach the datasource. HTTP response code: ' + str(request.status_code))
        else:
            return request.json()


class FileJsonDataSource(object):
    """Class for providing json data from json files."""

    FILE_OPEN_METHOD = 'rt'
    DEFAULT_ENCODING = 'utf8'

    def __init__(self, file_path, encoding_str=DEFAULT_ENCODING):
        self.file_path = file_path
        self.encoding_str = encoding_str

    def get_data(self):
        with io.open(self.file_path, FileJsonDataSource.FILE_OPEN_METHOD, encoding=self.encoding_str) as data_file:
            return json.load(data_file)
