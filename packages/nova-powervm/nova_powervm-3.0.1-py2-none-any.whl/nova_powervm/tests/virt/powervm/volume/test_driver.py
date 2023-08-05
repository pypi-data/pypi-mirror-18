# Copyright 2015 IBM Corp.
#
# All Rights Reserved.
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

import mock

from nova import test


class TestVolumeAdapter(test.TestCase):

    def setUp(self):
        super(TestVolumeAdapter, self).setUp()

        # Enable passing through the can attach/detach checks
        self.mock_get_inst_wrap_p = mock.patch('nova_powervm.virt.powervm.vm.'
                                               'get_instance_wrapper')
        self.mock_get_inst_wrap = self.mock_get_inst_wrap_p.start()
        self.addCleanup(self.mock_get_inst_wrap_p.stop)
        self.mock_inst_wrap = mock.MagicMock()
        self.mock_inst_wrap.can_modify_io.return_value = (True, None)
        self.mock_get_inst_wrap.return_value = self.mock_inst_wrap
