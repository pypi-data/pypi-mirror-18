# Copyright 2016 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from keystoneauth1.identity import v2
from keystoneauth1 import session
import logging
import os_client_config

logging.basicConfig(level=logging.INFO, format='%(message)s')


class RedScaleApp(object):

    def __init__(self, name, parser):
        self.name = name
        self.extend_parser(parser)
        self.args = self.parser.parse_args()

    @staticmethod
    def extend_parser(parser):
        """Extend specific app parser with these general argument(s)"""
        parser.add_argument('--cloud', '-c', dest='cloud', required=True,
                            help='the name of the cloud')

    @staticmethod
    def create_auth(cloud_name):
        """Returns keystone auth."""
        cloud = os_client_config.OpenStackConfig().get_one_cloud(cloud_name)

        auth = v2.Password(
            auth_url=cloud.config['auth']['auth_url'],
            username=cloud.config['auth']['username'],
            password=cloud.config['auth']['password'],
            tenant_name=cloud.config['auth']['project_name'])

        return auth

    @staticmethod
    def create_session(auth):
        return session.Session(auth=auth, verify=False)
