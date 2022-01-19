# This code shows using python requests module and HTTPBasicAuth
# we can connect redfish server and get data by calling redfish api.

import json
import requests
from requests.auth import HTTPBasicAuth
import ssl

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

# When running remotely connect using the address, account name,
# and password to send https requests
login_host = "https://****/"
login_account = "*****"
login_password = "******"

url = login_host + "redfish/v1/Systems"
print(url)

auth = HTTPBasicAuth(login_account, login_password)
response = requests.get(url, auth=auth, verify=False)

jsonData = json.loads(response.text)

print(jsonData)
