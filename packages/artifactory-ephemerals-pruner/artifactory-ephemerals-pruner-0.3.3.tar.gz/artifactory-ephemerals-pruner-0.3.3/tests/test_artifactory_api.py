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

import os
import json
import mock
import unittest

from hamcrest import assert_that, has_item, has_length, is_, is_not
from artifactory_ephemerals_pruner.artifactory_api import ArtifactoryApi


class TestArtifactoryApi(unittest.TestCase):
    def setUp(self):
        self.artifactory_api = ArtifactoryApi(
            artifactory_url='http://artifactory.invalid/artifactory/api',
            user='admin',
            password='admin')

    @mock.patch('requests.get')
    def test_find_subfolders_works(self, mock_get):
        mock_get.return_value = MockResponse(
            self.load_fixture('get_sub_folders.json'), 200)
        sub_folders = self.artifactory_api.find_subfolders('root')
        assert_that(sub_folders, has_item('/ironic-sync'))
        assert_that(sub_folders, has_item('/keysmith'))
        assert_that(sub_folders, has_item('/monthly-python'))

    @mock.patch('requests.get')
    def test_obtain_repository_list(self, mock_get):
        mock_get.return_value = MockResponse(
            self.load_fixture('get_sub_repositories.json'), 200)
        expected_repos = ['internap/ironic-sync', 'internap/keysmith',
                          'internap/monthly-python']
        actual_repositories = self.artifactory_api.get_sub_repositories(
            'local-docker')
        assert_that(actual_repositories, has_item(expected_repos[0]))
        assert_that(actual_repositories, has_item(expected_repos[1]))
        assert_that(actual_repositories, has_item(expected_repos[2]))

    @mock.patch('requests.get')
    def test_obtain_tags_from_repository(self, mock_get):
        mock_get.return_value = MockResponse(
            self.load_fixture('tags_list.json'), 200)
        tags = self.artifactory_api.get_tags('local-docker', 'ironic-sync')
        assert_that(tags, has_item('1.1.222'))

    @mock.patch('requests.get')
    def test_get_ephemeral_tags(self, mock_get):
        mock_get.return_value = MockResponse(
            self.load_fixture('tags_list.json'), 200)
        tags = self.artifactory_api.get_tags('local-docker', 'ironic-sync')
        ephemeral_tags = \
            self.artifactory_api.filter_ephemerals(tags,
                                                   '[0-9]\.[0-9]\.[0-9]*\.[Z]')
        assert_that(ephemeral_tags, has_length(7))
        assert_that(ephemeral_tags,
                    has_item('1.0.229.Zad03d3aea5784e1c99ba12eb831e8152'))
        assert_that(ephemeral_tags, is_not(has_item('1.1.222')))

    @mock.patch('requests.get')
    def test_delete_ephemeral_version(self, mock_get):
        mock_get.side_effect = [
            MockResponse(self.load_fixture('tags_list.json'), 200),
            MockResponse('{}', 202)
        ]
        tags = self.artifactory_api.get_tags('local-docker', 'ironic-sync')
        ephemeral_tags = \
            self.artifactory_api.filter_ephemerals(tags,
                                                   '[0-9]\.[0-9]\.[0-9]*\.[Z]')

        assert_that(
            self.artifactory_api.delete_tag('local-docker', 'ironic-sync',
                                            ephemeral_tags[0]), is_(True))

    def load_fixture(self, filename):
        with open(os.path.join(os.getcwd(),
                               'tests/fixtures/{}'.format(filename))) as json_data:
            return json.dumps(json.load(json_data))


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data
