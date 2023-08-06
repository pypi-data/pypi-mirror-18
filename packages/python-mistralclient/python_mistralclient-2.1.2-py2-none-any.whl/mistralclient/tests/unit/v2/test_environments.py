# Copyright 2015 - StackStorm, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import collections
import copy
import json

import pkg_resources as pkg
from six.moves.urllib import parse
from six.moves.urllib import request

from mistralclient.api.v2 import environments
from mistralclient.tests.unit.v2 import base
from mistralclient import utils


ENVIRONMENT = {
    'name': 'env1',
    'description': 'Test Environment #1',
    'scope': 'private',
    'variables': {
        'server': 'localhost'
    }
}

URL_TEMPLATE = '/environments'
URL_TEMPLATE_NAME = '/environments/%s'


class TestEnvironmentsV2(base.BaseClientV2Test):

    def test_create(self):
        data = copy.deepcopy(ENVIRONMENT)

        mock = self.mock_http_post(content=data)
        env = self.environments.create(**data)

        self.assertIsNotNone(env)

        expected_data = copy.deepcopy(data)
        expected_data['variables'] = json.dumps(expected_data['variables'])

        mock.assert_called_once_with(URL_TEMPLATE, json.dumps(expected_data))

    def test_create_with_json_file_uri(self):
        # The contents of env_v2.json must be equivalent to ENVIRONMENT
        path = pkg.resource_filename(
            'mistralclient',
            'tests/unit/resources/env_v2.json'
        )

        # Convert the file path to file URI
        uri = parse.urljoin('file:', request.pathname2url(path))
        data = collections.OrderedDict(
            utils.load_content(
                utils.get_contents_if_file(uri)
            )
        )

        mock = self.mock_http_post(content=data)
        file_input = {'file': uri}
        env = self.environments.create(**file_input)

        self.assertIsNotNone(env)

        expected_data = copy.deepcopy(data)
        expected_data['variables'] = json.dumps(expected_data['variables'])

        mock.assert_called_once_with(URL_TEMPLATE, json.dumps(expected_data))

    def test_update(self):
        data = copy.deepcopy(ENVIRONMENT)

        mock = self.mock_http_put(content=data)
        env = self.environments.update(**data)

        self.assertIsNotNone(env)

        expected_data = copy.deepcopy(data)
        expected_data['variables'] = json.dumps(expected_data['variables'])

        mock.assert_called_once_with(URL_TEMPLATE, json.dumps(expected_data))

    def test_update_with_yaml_file(self):
        # The contents of env_v2.json must be equivalent to ENVIRONMENT
        path = pkg.resource_filename(
            'mistralclient',
            'tests/unit/resources/env_v2.json'
        )
        data = collections.OrderedDict(
            utils.load_content(
                utils.get_contents_if_file(path)
            )
        )

        mock = self.mock_http_put(content=data)
        file_input = {'file': path}
        env = self.environments.update(**file_input)

        self.assertIsNotNone(env)

        expected_data = copy.deepcopy(data)
        expected_data['variables'] = json.dumps(expected_data['variables'])

        mock.assert_called_once_with(URL_TEMPLATE, json.dumps(expected_data))

    def test_list(self):
        mock = self.mock_http_get(content={'environments': [ENVIRONMENT]})

        environment_list = self.environments.list()

        self.assertEqual(1, len(environment_list))

        env = environment_list[0]

        self.assertDictEqual(
            environments.Environment(self.environments, ENVIRONMENT).to_dict(),
            env.to_dict()
        )

        mock.assert_called_once_with(URL_TEMPLATE)

    def test_get(self):
        mock = self.mock_http_get(content=ENVIRONMENT)

        env = self.environments.get('env')

        self.assertIsNotNone(env)
        self.assertDictEqual(
            environments.Environment(self.environments, ENVIRONMENT).to_dict(),
            env.to_dict()
        )

        mock.assert_called_once_with(URL_TEMPLATE_NAME % 'env')

    def test_delete(self):
        mock = self.mock_http_delete(status_code=204)

        self.environments.delete('env')

        mock.assert_called_once_with(URL_TEMPLATE_NAME % 'env')
