Shared storage provides a global namespace across the CORTX cluster. The global name space would come from clustered file system like Glusterfs

Get Shared Storage path

This will provide the shared storage path (global namespace) available on the node/cluster.

API Specification -

from cortx.utils.shared_storage import Storage

# name - the directory name required to be created inside shared path (mount-point), if none, returns the shared path/mountpoint
# exist_ok - If set to False, SharedStorageError is raised if directory name passed in already present.

# path will be none if no shared storage available

path = Storage.get_path(name=None, exist_ok=True)

Example -

from cortx.utils.shared_storage import Storage

# return the mount point/shared path as is:
path = Storage.get_path()

# creates a directory named 'dir_name' in shared path and return its path.
path = Storage.get_path(name='dir_name', exist_ok=True)

