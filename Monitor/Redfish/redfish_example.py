# This code is example of redfish python library module.
# Using redfish module we can directly connect to server and
# by calling api get response.
# Authentication used here is session based.

import redfish
import json

# When running remotely connect using the address, account name,
# and password to send https requests

login_host = "https://server_ip"
login_account = "username"
login_password = "password"

# Create a REDFISH object
REDFISH_OBJ = redfish.redfish_client(base_url=login_host,
                                     username=login_account,
                                     password=login_password)

# Login into the server and create a session
REDFISH_OBJ.login(auth="session")

# Do a GET on a given path
response = REDFISH_OBJ.get("/redfish/v1/Chassis")

# Print out the response
print("%s\n" % response.text)

data = json.loads(response.text)

#Get members of chassis
print(data['Members'])

print(response.status)

# Logout of the current session
REDFISH_OBJ.logout()
