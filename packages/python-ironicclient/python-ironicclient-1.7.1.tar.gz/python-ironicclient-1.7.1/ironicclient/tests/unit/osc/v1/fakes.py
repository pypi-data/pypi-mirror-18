#
#   Copyright 2015 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import mock
from osc_lib.tests import utils

from ironicclient.tests.unit.osc import fakes

baremetal_chassis_uuid = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'
baremetal_chassis_description = 'chassis description'
baremetal_chassis_extra = {}
BAREMETAL_CHASSIS = {
    'uuid': baremetal_chassis_uuid,
    'description': baremetal_chassis_description,
    'extra': baremetal_chassis_extra,
}

baremetal_uuid = 'xxx-xxxxxx-xxxx'
baremetal_name = 'fake name'
baremetal_instance_uuid = 'yyy-yyyyyy-yyyy'
baremetal_power_state = None
baremetal_provision_state = None
baremetal_maintenance = False

BAREMETAL = {
    'uuid': baremetal_uuid,
    'name': baremetal_name,
    'instance_uuid': baremetal_instance_uuid,
    'power_state': baremetal_power_state,
    'provision_state': baremetal_provision_state,
    'maintenance': baremetal_maintenance,
    'links': []
}

baremetal_port_uuid = 'zzz-zzzzzz-zzzz'
baremetal_port_address = 'AA:BB:CC:DD:EE:FF'
baremetal_port_extra = {'key1': 'value1',
                        'key2': 'value2'}

BAREMETAL_PORT = {
    'uuid': baremetal_port_uuid,
    'address': baremetal_port_address,
    'extra': baremetal_port_extra,
    'node_uuid': baremetal_uuid,
}

baremetal_driver_hosts = ['fake-host1', 'fake-host2']
baremetal_driver_name = 'fakedrivername'

BAREMETAL_DRIVER = {
    'hosts': baremetal_driver_hosts,
    'name': baremetal_driver_name,
}

baremetal_driver_passthru_method = 'lookup'

BAREMETAL_DRIVER_PASSTHRU = {"lookup": {"attach": "false",
                                        "http_methods": ["POST"],
                                        "description": "",
                                        "async": "false"}}


class TestBaremetal(utils.TestCommand):

    def setUp(self):
        super(TestBaremetal, self).setUp()

        self.app.client_manager.auth_ref = mock.Mock(auth_token="TOKEN")
        self.app.client_manager.baremetal = mock.Mock()


class FakeBaremetalResource(fakes.FakeResource):

    def get_keys(self):
        return {'property': 'value'}
