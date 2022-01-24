# CORTX Python common library.
# Copyright (c) 2021 Seagate Technology LLC and/or its Affiliates
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

import inspect
import errno
from urllib.parse import urlparse

from cortx.utils import errors
from cortx.utils.shared_storage import SharedStorageError

class SharedStorageAgent:

    """ A common interface over all shared storage agents """

    def _fetch_path(self):
        """ fetch path from source """
        raise SharedStorageError(errno.EINVAL, \
                "_fetch_path not implemented")

    def get_path(self):
        """ return fetched path of shared storage mountpoint """
        shared_path = self._fetch_path()
        return shared_path


class SharedStorageFactory:

    """ Factory class for shared storage types """

    _storages = {}

    @staticmethod
    def get_instance(shared_storage_url: str) -> SharedStorageAgent:
        """ Obtain instance of SharedStorageAgent for given file_type """

        try:
            url_spec = urlparse(shared_storage_url)
        except Exception as e:
            raise SharedStorageError(errno.EINVAL, \
                "Invalid path: %s. %s", shared_storage_url, e)
        storage_type = url_spec.scheme
        shared_loc = url_spec.netloc
        shared_path = url_spec.path

        if storage_type in SharedStorageFactory._storages:
            return SharedStorageFactory._storages[storage_type]

        from cortx.utils.shared_storage import shared_storage_collection
        agents = inspect.getmembers(shared_storage_collection, inspect.isclass)
        for name, cls in agents:
            if name.endswith('Storage'):
                if storage_type == cls.name:
                    storage_agent = cls(shared_path)
                    SharedStorageFactory._storages[storage_type] = storage_agent
                    return storage_agent

        raise SharedStorageError(errors.ERR_INVALID_SERVICE_NAME, \
            "Invalid service name %s.", storage_type)