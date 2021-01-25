Running s3server in full fake mode to get the bets performance result
=====================================================================

Run S3 in full-fake mode on hardware (single node) and capture latency/TTFB
that we currently observe, to see if there are bottlenecks in S3 components
(S3server, Auth, ldap).


Corresponding Jira Ticket
=========================

https://jts.seagate.com/browse/EOS-15899


Objectives
==========

Run S3 release configuration in full fake mode on a single HW node.
Number of S3 instances should be set to ~30% of CPU cores.
Number of clients should be ranged from 1 per node to 600 per node.
Measure performance metrics during the load with objects of different sizes
ranging from small to big.


POC Details
===========

HW node has 96 CPUs and 376GB of RAM.
Approximate number of s3 instances should be 31.
With 600 concurrent clients and even load distribution each instance should
process ~20 concurrent connections.

To simplify test and get the best from S3server it was decided to use following
configuration

* S3
  * single S3server instance
  * release configuration
  * full fake mode

* Clients
  * S3bench
  * number of clients are 1, 5, 10, 15, 20
  * object sizes are 1KB, 16KB, 256KB, 1MB, 16MB, 256MB
  * number of objects per test session is 10000
  * single test session for 1 client, 5 objects of 50GB size


Results
=======

| cfg                 | operation | RPS      | ttfb_avg | ttfb_99th-ile |
| ------------------- | ---------- | -------- | --------- | -------------- |
| 1c_10ko_1kb.json    | "Read"    | 24.19133 | 0.041307  | 0.080861       |
| 5c_10ko_1kb.json    | "Read"    | 135.2289 | 0.036919  | 0.100477       |
| 10c_10ko_1kb.json   | "Read"    | 219.8465 | 0.045367  | 0.118401       |
| 15c_10ko_1kb.json   | "Read"    | 273.6465 | 0.05468   | 0.127889       |
| 20c_10ko_1kb.json   | "Read"    | 311.7695 | 0.063945  | 0.147809       |
| 1c_10ko_16kb.json   | "Read"    | 19.76697 | 0.011209  | 0.026783       |
| 5c_10ko_16kb.json   | "Read"    | 81.33929 | 0.022432  | 0.091277       |
| 10c_10ko_16kb.json  | "Read"    | 139.2336 | 0.040001  | 0.110527       |
| 15c_10ko_16kb.json  | "Read"    | 196.5243 | 0.047497  | 0.120351       |
| 20c_10ko_16kb.json  | "Read"    | 244.1803 | 0.0548    | 0.128844       |
| 1c_10ko_256kb.json  | "Read"    | 20.86561 | 0.03137   | 0.061578       |
| 5c_10ko_256kb.json  | "Read"    | 93.49564 | 0.026964  | 0.086804       |
| 10c_10ko_256kb.json | "Read"    | 144.9676 | 0.03708   | 0.107002       |
| 15c_10ko_256kb.json | "Read"    | 187.7361 | 0.04459   | 0.121507       |
| 20c_10ko_256kb.json | "Read"    | 221.8321 | 0.052823  | 0.135124       |
| 1c_10ko_1mb.json    | "Read"    | 32.94456 | 0.011099  | 0.025136       |
| 5c_10ko_1mb.json    | "Read"    | 84.73036 | 0.028872  | 0.101992       |
| 10c_10ko_1mb.json   | "Read"    | 131.9877 | 0.039249  | 0.107683       |
| 15c_10ko_1mb.json   | "Read"    | 156.4147 | 0.051416  | 0.130315       |
| 20c_10ko_1mb.json   | "Read"    | 188.3134 | 0.056371  | 0.135969       |
| 1c_10ko_16mb.json   | "Read"    | 13.25416 | 0.031001  | 0.074284       |
| 5c_10ko_16mb.json   | "Read"    | 32.87285 | 0.050936  | 0.152974       |
| 10c_10ko_16mb.json  | "Read"    | 46.11623 | 0.070138  | 0.218248       |
| 15c_10ko_16mb.json  | "Read"    | 52.61389 | 0.087271  | 0.287651       |
| 20c_10ko_16mb.json  | "Read"    | 58.75192 | 0.091361  | 0.357711       |
| 1c_10ko_256mb.json  | "Read"    | 1.646464 | 0.179798  | 0.323005       |
| 5c_10ko_256mb.json  | "Read"    | 4.352237 | 0.121715  | 0.638872       |
| 10c_10ko_256mb.json | "Read"    | 6.133868 | 0.094621  | 0.434314       |
| 15c_10ko_256mb.json | "Read"    | 6.163513 | 0.095059  | 0.393876       |
| 20c_10ko_256mb.json | "Read"    | 6.031245 | 0.097139  | 0.395326       |
| 1c_5o_50gb.json     | "Read"    | 0.010054 | 33.9326   | 36.19711       |


Detailed results could be found in [report](../doc/report.csv) and
[histogram for all tests together](../doc/m0db_tests_hist.png).

Shared [excel report](https://seagatetechnology.sharepoint.com/:x:/r/sites/gteamdrv1/tdrive1224/_layouts/15/doc2.aspx?sourcedoc=%7B9896f554-9380-4505-be06-a7f0cf0bade5%7D&action=edit&wdPreviousSession=e899fdec-292b-42d9-8f14-02f46a81336c&cid=850b7e27-b3d8-46ee-8523-feae709b83ce)
