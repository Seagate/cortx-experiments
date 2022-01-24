#!/usr/bin/env python3

# CORTX Python common library.
# Copyright (c) 2021 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.

import os
import unittest

from cortx.utils.shared_storage import Storage
from cortx.utils.conf_store import Conf

class TestSharedStorage(unittest.TestCase):

    """ Unit test class to test shared storage. """

    @classmethod
    def setUpClass(cls):
        """Register the test message_type."""
        config_file = 'json:///etc/cortx/cortx.conf'
        Conf.load('cotrx_config', config_file, skip_reload=True)
        cls.local_path = Conf.get('cotrx_config', 'support>local_path')
        os.makedirs(cls.local_path, exist_ok=True)

    def test_shared_path_read_access(self):
        """ test if shared storage path exists and is readable """
        shared_path = Storage.get_path()
        if not shared_path:
            shared_path=TestSharedStorage.local_path
        self.assertTrue(os.access(shared_path, os.R_OK))

    def test_shared_path_write_access(self):
        """ test if shared storage path exists and is writable """
        shared_path = Storage.get_path()
        if not shared_path:
            shared_path=TestSharedStorage.local_path
        self.assertTrue(os.access(shared_path, os.W_OK))



if __name__ == '__main__':
    unittest.main()