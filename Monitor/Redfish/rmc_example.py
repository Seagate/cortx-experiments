# RMC(Remote Monitor Controller) is Redfish interface for
# schema validation, caching, and error registries.
# As per below code, by using RMCApp object no need to
# call actual api just by calling get function with
# perticular selector can obtain data.

import os
import time
from redfish.ris.rmc import RmcApp
App = RmcApp([])

# When running remotely connect using the address, account name,
# and password to send https requests
login_host = "https://server_ip/"
login_account = "username"
login_password = "password"

config_dir = r'C:\redfish_cache'
App.config.set_cachedir(os.path.join(config_dir, 'cache'))
cachedir = App.config.get_cachedir()
start_time = time.time()
App.login(base_url=login_host, username=login_account,
          password=login_password)

end_time = time.time()
print("Time to take login server : ")
print(end_time - start_time)

data = App.select(["ComputerSystem."])
print(App.get())

App.logout()
