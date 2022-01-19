# Objective

 DMTF orgnization provides python3 library redfish for interacting with devices that support a Redfish service. Using this library we can connect server and call Redfish API.

Python already have urllib and requests modules which can be used for fetching URLs using a variety of different protocols.

This experiment checks which python library will be more suitable to get data via redfish apis for monitoring.

## Observation

 Redfish python library itself is using urllib.parse module to fetach URIs of redfish.
 
 Its need to install redfish module using pip command 'pip install redfish'

 Whereas requests python module is not native python library, it needs to install manually.
 
 requests uses urllib under the hood and used to retrieve data from API response.

 urllib is original Python HTTP client, the standard native library, can use to avoid adding any dependencies.

 urllib.request is accepting a Request object to set the headers for a URL request.
 urllib provides the urlencode method which is used for the generation of GET query string.

urllib returns an object of type <class http.client.HTTPResponse> whereas requests returns <class 'requests.models.Response'>.

Due to this, read() method can be used with urllib but not with requests.
  
redfish python library returns own class type : <class 'redfish.rest.v1.RestResponse'> but this class also wrapper for HTTPResponse.
  
## Conclusion

To avoid third party library dependancies, should prefer urllib python modules, as its base of other libraries (redfish, requests) which is useful to call RestAPI and get Response. 
