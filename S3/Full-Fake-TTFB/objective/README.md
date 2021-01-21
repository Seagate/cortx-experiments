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

| cfg                 | operation | RPS         | ttfb_99th-ile |
| ------------------- | ---------- | ----------- | -------------- |
| 1c_10ko_1kb.json    | "Read"    | 24.19132858 | 0.080861       |
| 5c_10ko_1kb.json    | "Read"    | 135.228867  | 0.100477       |
| 10c_10ko_1kb.json   | "Read"    | 219.8465361 | 0.118401       |
| 15c_10ko_1kb.json   | "Read"    | 273.6464761 | 0.127889       |
| 20c_10ko_1kb.json   | "Read"    | 311.7694657 | 0.147809       |
| 1c_10ko_16kb.json   | "Read"    | 19.76697137 | 0.026783       |
| 5c_10ko_16kb.json   | "Read"    | 81.33928715 | 0.091277       |
| 10c_10ko_16kb.json  | "Read"    | 139.2336469 | 0.110527       |
| 15c_10ko_16kb.json  | "Read"    | 196.5243026 | 0.120351       |
| 20c_10ko_16kb.json  | "Read"    | 244.1802924 | 0.128844       |
| 1c_10ko_256kb.json  | "Read"    | 20.86561339 | 0.061578       |
| 5c_10ko_256kb.json  | "Read"    | 93.49564102 | 0.086804       |
| 10c_10ko_256kb.json | "Read"    | 144.967583  | 0.107002       |
| 15c_10ko_256kb.json | "Read"    | 187.7360628 | 0.121507       |
| 20c_10ko_256kb.json | "Read"    | 221.8320541 | 0.135124       |
| 1c_10ko_1mb.json    | "Read"    | 32.94456159 | 0.025136       |
| 5c_10ko_1mb.json    | "Read"    | 84.73036046 | 0.101992       |
| 10c_10ko_1mb.json   | "Read"    | 131.9877098 | 0.107683       |
| 15c_10ko_1mb.json   | "Read"    | 156.4146998 | 0.130315       |
| 20c_10ko_1mb.json   | "Read"    | 188.3133914 | 0.135969       |
| 1c_10ko_16mb.json   | "Read"    | 13.25416407 | 0.074284       |
| 5c_10ko_16mb.json   | "Read"    | 32.87285271 | 0.152974       |
| 10c_10ko_16mb.json  | "Read"    | 46.11623163 | 0.218248       |
| 15c_10ko_16mb.json  | "Read"    | 52.61389486 | 0.287651       |
| 20c_10ko_16mb.json  | "Read"    | 58.75192188 | 0.357711       |
| 1c_10ko_256mb.json  | "Read"    | 1.646463799 | 0.323005       |
| 5c_10ko_256mb.json  | "Read"    | 4.352237094 | 0.638872       |
| 10c_10ko_256mb.json | "Read"    | 6.133868307 | 0.434314       |
| 15c_10ko_256mb.json | "Read"    | 6.163512601 | 0.393876       |
| 20c_10ko_256mb.json | "Read"    | 6.031244871 | 0.395326       |
| 1c_5o_50gb.json     | "Read"    | 0.010054164 | 36.197109      |


Detailed results could be found in [report](../doc/report.csv) and
[histogram](../doc/m0db_tests_hist.png).

Shared [excel report](https://seagatetechnology.sharepoint.com/:x:/r/sites/gteamdrv1/tdrive1224/_layouts/15/doc2.aspx?sourcedoc=%7B9896f554-9380-4505-be06-a7f0cf0bade5%7D&action=edit&wdPreviousSession=e899fdec-292b-42d9-8f14-02f46a81336c&cid=850b7e27-b3d8-46ee-8523-feae709b83ce)
