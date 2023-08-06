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

import urlparse

import xnat

import fastr
from fastr.plugins import XNATStorage


class QIBSession(XNATStorage):
    """
    Will write sink data to a QIB Session type on an XNAT server
    """
    scheme = ('qib', 'qibs')

    # qib://xnat.bmia.nl/data/archive/projects/project/subjects/subject/experiments/qiblabel
    # qibs://xnat.bmia.nl/data/archive/projects/project/subjects/subject/experiments/qiblabel

    def __init__(self):
        # initialize the instance and register the scheme
        super(QIBSession, self).__init__()

    def put_url(self, inpath, outurl):
        """
        Put the files to the external data store.

        :param inpath: path of the local data
        :param outurl: url to where to store the data, starts with ``file://``
        """
        url = urlparse.urlparse(outurl)

        path_prefix = url.path[:url.path.find('/data/archive')]
        url = url._replace(path=url.path[len(path_prefix):])  # Strip the prefix of the url path
        outurl = urlparse.urlunparse(url)

        insecure = (url.scheme == 'qib')
        use_regex = urlparse.parse_qs(url.query).get('regex', ['0'])[0] in ['true', '1']
        self.connect(url.netloc, path=path_prefix, insecure=insecure)

        # Determine the resource to upload to
        resource = self._locate_resource(outurl,
                                         create=True,
                                         use_regex=use_regex,
                                         resource_cls=self.xnat.XNAT_CLASS_LOOKUP['bigr:QIBSession'])

        # Upload the file
        fastr.log.info('Uploading to: {}'.format(resource.fulluri))
        try:
            self.xnat.upload(resource.fulluri, inpath)
            return True
        except xnat.exceptions.XNATUploadError as exception:
            fastr.log.error('Encountered error when uploading data: {}'.format(exception))
            return False
