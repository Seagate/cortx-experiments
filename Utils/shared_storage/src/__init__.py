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

__title__ = 'shared_storage'

from cortx.utils.shared_storage.error import SharedStorageError
from cortx.utils.shared_storage.shared_storage_agent import SharedStorageAgent
from cortx.utils.shared_storage.shared_storage import Storage

__doc__ = """
Shared storage framework

This framework is a tool to fetch the shared storage available in the environment.
It fetches the shared path from a conf file and returns it to the caller. 

module: Storage"""

__all__ = [SharedStorageError, SharedStorageAgent, Storage]