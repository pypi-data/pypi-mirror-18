# Copyright 2011-2014 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains the Null plugin for fastr
"""

from fastr.core.ioplugin import IOPlugin


class HttpRequest(IOPlugin):
    """
    The Http plugin is create to handle ``http://``, ``https://` type or URLs.
    These URLs can be augmented using a method using a scheme is the form of
    ``http+method://`` or ``https+method://`` where method can be one of
    ``get``, ``put``, ``post``, or ``delete``. For example ``http+post://``
    will generate a post request.
    """
    scheme = ('http', 'http+get', 'http+put', 'http+post', 'http+delete',
              'https', 'https+get', 'https+put', 'https+post', 'https+delete')

    def __init__(self):
        # initialize the instance and register the scheme
        super(HttpRequest, self).__init__()

    def put_url(self, inpath, outurl):
        """
        Put the files to the external data store.

        :param inpath: path of the local data
        :param outurl: url to where to store the data, starts with ``file://``
        """
        return True

    def put_value(self, value, outurl):
        """
        Put the value in the external data store.

        :param value: value to store
        :param outurl: url to where to store the data, starts with ``file://``
        """
        return True
