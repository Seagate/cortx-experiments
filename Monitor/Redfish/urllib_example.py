# This code is example of urllib usage.
# Using urllib library module we can call
# redfish API and get HTTPResponse.
import json
import urllib.request
import base64
import requests
import ssl

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

# When running remotely connect using the address, account name,
# and password to send https requests
login_host = "https://****"
login_account = "*****"
login_password = "*****"

request = urllib.request.Request(login_host)
creds = "%s:%s" % (login_account, login_password)
base64string = base64.b64encode(creds.encode())
print(base64string)

request.add_header("Authorization", "Basic %s" % base64string.decode())

response = urllib.request.urlopen(request)
print(response.status)

jsonData = json.loads(response.read())
print(jsonData)
