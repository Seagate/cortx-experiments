EOS-16557 - Create load test tool for AuthServer capable of 4k RPS

Goal:
Determine if AuthServer can be tuned to sustain 4000 S3 API requests per second

Development:
Previously, we had used Locust to generate the load.But Locust, since it is using 
python libraries was not able to scale to a high RPS.
So, a C++ load generator was used.
- Requests were generated using the CURL library.
- For Digital Signing, part of the code were used from Amazon C++ SDK and from 
  https://github.com/rhymu8354/Aws
- Client/Server framework in https://github.com/Seagate/cortx-s3server/tree/main/scripts/libevhtp-throughput was used to send the requests.
- The client issues "ListAccount" requests to the authserver 

Environment Details:
Testing was performed on Dev VM and then on R1 HW
For Testing plain HTTP requests were issued with NO SSL

PoC Observations:
On R1 HW, the auth server can successfully respond to 4000 requests per second.

Further Work:
Secret Key should be coming in as a command line parameter.Currently, it is hardcoded in the code
Currently, all requests came from a single S3 user.
Next, they need to come from multiple different S3 users – e.g. 32 or 100.
