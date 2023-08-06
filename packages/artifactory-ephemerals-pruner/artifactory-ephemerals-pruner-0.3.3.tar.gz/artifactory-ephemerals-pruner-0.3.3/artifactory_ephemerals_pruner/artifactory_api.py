# Copyright 2016 Internap.
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

import re
import json
import requests
from requests.auth import HTTPBasicAuth


class ArtifactoryApi():
    def __init__(self, artifactory_url, user, password):
        self.artifactory_url = artifactory_url
        self.user = user
        self.password = password

    def find_subfolders(self, repository):
        url = "{0}/storage/{1}".format(self.artifactory_url, repository)
        _, data = self.api_call(url)
        return [child['uri'] for child in data['children']]

    def get_sub_repositories(self, repository):
        url = "{0}/docker/{1}/v2/_catalog".format(self.artifactory_url,
                                                  repository)
        _, data = self.api_call(url)
        return [repository for repository in data['repositories']]

    def get_tags(self, repository, sub_repository):
        url = "{0}/docker/{1}/v2/internap/{2}/tags/list".format(
            self.artifactory_url, repository, sub_repository)
        _, data = self.api_call(url)
        return [tag for tag in data['tags']]

    def filter_ephemerals(self, tags, pattern):
        return [tag for tag in tags if re.match(pattern, tag)]

    def delete_tag(self, repository, sub_repository, tag):
        url = "{0}/docker/{1}/v2/internap/{2}/manifests/{3}".format(
            self.artifactory_url,
            repository,
            sub_repository,
            tag)
        code, data = self.api_call(url)
        return code == 202

    def api_call(self, url):
        r = requests.get(url, auth=HTTPBasicAuth(self.user, self.password))
        data = json.loads(r.json())
        return r.status_code, data
