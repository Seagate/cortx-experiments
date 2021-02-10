Running s3server in full fake mode to get the bets performance result
=====================================================================

Run S3 in full-fake mode on hardware (single node) and capture latency/TTFB
that we currently observe, to see if there are bottlenecks in S3 components
(S3server, Auth, LDAP).

Contents:

- [Running s3server in full fake mode to get the bets performance result](#running-s3server-in-full-fake-mode-to-get-the-bets-performance-result)
- [Corresponding Jira Ticket](#corresponding-jira-ticket)
- [Objectives](#objectives)
- [POC Details](#poc-details)
- [Results](#results)
- [Analysis](#analysis)
  - [Intro](#intro)
  - [TTFB](#ttfb)
  - [Throughput](#throughput)


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

HW node has 96 CPUs and 376GB of RAM.  This is single R2-spec'd server node.

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

| Configuration       | operation | RPS      | ttfb_avg  | ttfb_99th-ile  |
| ------------------- | --------- | -------- | --------- | -------------- |
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


Detailed results could be found in [report](report.csv) and
[histogram for all tests together](m0db_tests_hist.png).

Shared [excel report](https://seagatetechnology.sharepoint.com/:x:/r/sites/gteamdrv1/tdrive1224/_layouts/15/doc2.aspx?sourcedoc=%7B9896f554-9380-4505-be06-a7f0cf0bade5%7D&action=edit&wdPreviousSession=e899fdec-292b-42d9-8f14-02f46a81336c&cid=850b7e27-b3d8-46ee-8523-feae709b83ce)


Analysis
========

Intro
-----

"Full Fake" is a nick name for a special mode in S3 server when most of Motr
calls are stubbed out and are not directed to Motr but are "faked", i.e. their
results are "fake" (hard coded).  Motr KVS is replaced with in-memory KVS (kept
as `std::map` in S3 memory).  Motr IO is not done; incoming data is just
discarded, outcoming data is filled with "all zeroes".

Notes:

* Since KVS is kept in memory of an S3 process, there is no easy way to launch
  multiple S3 instances.  So we're testing with single instance, and it should
  be then extrapolated to multiple instances.
* Not all of the Motr calls are stubbed out, some interaction is still
  happening, so it's not true "full fake" (which might explain some of the
  observations).

The aim of this POC was to see what performance we can achieve in "isolated"
environment, abstracted from possible latencies and limitations of the
underlying storage engine (Motr).

TTFB
----

DR level set for TTFB is: 99% of read requests must see first byte of data
within 150ms.

Summary table on TTFB (Time to First Byte):

| `objectSize` (MB) | `objectSize` | `numClients` | `ttfb_avg` (ms) | `ttfb_99th-ile` (ms) |
| ---------- | ---------: | ---------: | ------------: | -----------------: |
| 0.000977   | 1 KB       | 1          | 41            | 81                 |
| 0.000977   | 1 KB       | 5          | 37            | 100                |
| 0.000977   | 1 KB       | 10         | 45            | 118                |
| 0.000977   | 1 KB       | 15         | 55            | 128                |
| 0.000977   | 1 KB       | 20         | 64            | 148                |
| 0.015625   | 16 KB      | 1          | 11            | 27                 |
| 0.015625   | 16 KB      | 5          | 22            | 91                 |
| 0.015625   | 16 KB      | 10         | 40            | 111                |
| 0.015625   | 16 KB      | 15         | 47            | 120                |
| 0.015625   | 16 KB      | 20         | 55            | 129                |
| 0.25       | 256 KB     | 1          | 31            | 62                 |
| 0.25       | 256 KB     | 5          | 27            | 87                 |
| 0.25       | 256 KB     | 10         | 37            | 107                |
| 0.25       | 256 KB     | 15         | 45            | 122                |
| 0.25       | 256 KB     | 20         | 53            | 135                |
| 1          | 1 MB       | 1          | 11            | 25                 |
| 1          | 1 MB       | 5          | 29            | 102                |
| 1          | 1 MB       | 10         | 39            | 108                |
| 1          | 1 MB       | 15         | 51            | 130                |
| 1          | 1 MB       | 20         | 56            | 136                |
| 16         | 16 MB      | 1          | 31            | 74                 |
| 16         | 16 MB      | 5          | 51            | 153                |
| 16         | 16 MB      | 10         | 70            | 218                |
| 16         | 16 MB      | 15         | 87            | 288                |
| 16         | 16 MB      | 20         | 91            | 358                |
| 256        | 256 MB     | 1          | 180           | 323                |
| 256        | 256 MB     | 5          | 122           | 639                |
| 256        | 256 MB     | 10         | 95            | 434                |
| 256        | 256 MB     | 15         | 95            | 394                |
| 256        | 256 MB     | 20         | 97            | 395                |
| 51200      | 50 GB      | 5          | 33932         | 36197              |

Notes:

* `ttfb_avg` is true average: `sum(samples) / count(samples)`.
* `numClients` is number of parallel sessions.
* S3 servers do not depend on each other, so when running multiple instances,
  TTFB latency from C++ code is supposed to stay the same.  But auth server is
  single instance for entire node, so multiple instances will share it, and that
  will add extra latency.  Needs separate POC.

Conclusions from the test results:

* Difference between average and 99th-ile is quite big (2-4 times).  There is a
  lot of outlier samples, so this has to be investigated further.
* Large objects definitely violate DR level of 150ms.
* At the same time, average values lie within the DR.  Except for 256MB 1 and 5
  clients (which anyway looks like a glitch and needs to be revisited -- compare
  with results on 10/15/20 clients which are showing better TTFB, which is not).
* Average value, even though within the DR, is still too high -- expectation is
  it should be smaller with full fake.
* TTFB is consistently growing with number of clients (as expected).
* With max clients (20) average TTFB was consistently about 50ms up to 1MB, and then
  almost doubled (91-97 ms).  It can be explained, but should not be happening
  -- needs further investigation.
* TTFB for the 50 GB test case exceeds 30 seconds. With small number of tests done
  it is difficult to explain these numbers. Further research is required and should
  include, besides addb analysis, experiments with memory pool parameters and
  memory pool profiling.


Throughput
----------

DR level set for throughput is:

* for objects of 256KB = 1GB/s read per node (implies 4k RPS);
* for objects of 16MB  = 3GB/s read per node.

! `objectSize` | `numClients` | Read RPS | Read throughput (MB/s) | Write RPS | Write throughput (MB/s) | R/W ratio |
| -----------: | -----------: | -------: | ---------------------: | --------: | ----------------------: | --------- |
| 1 KB         | 1            | 24.2     | 0.024                  | 38.3      | 0.037                   | 0.65      |
| 1 KB         | 5            | 135.2    | 0.132                  | 126.8     | 0.124                   | 1.06      |
| 1 KB         | 10           | 219.8    | 0.215                  | 189.9     | 0.185                   | 1.16      |
| 1 KB         | 15           | 273.6    | 0.267                  | 234.8     | 0.229                   | 1.17      |
| 1 KB         | 20           | 311.8    | 0.304                  | 268.7     | 0.262                   | 1.16      |
| 16 KB        | 1            | 19.8     | 0.309                  | 7.8       | 0.121                   | 2.55      |
| 16 KB        | 5            | 81.3     | 1.3                    | 40.5      | 0.632                   | 2.06      |
| 16 KB        | 10           | 139.2    | 2.2                    | 54.9      | 0.858                   | 2.56      |
| 16 KB        | 15           | 196.5    | 3.1                    | 74.0      | 1.157                   | 2.68      |
| 16 KB        | 20           | 244.2    | 3.8                    | 101.2     | 1.581                   | 2.40      |
| 256 KB       | 1            | 20.9     | 5.2                    | 24.0      | 6                       | 0.87      |
| 256 KB       | 5            | 93.5     | 23                     | 124.2     | 31                      | 0.74      |
| 256 KB       | 10           | 145.0    | 36                     | 174.0     | 44                      | 0.82      |
| 256 KB       | 15           | 187.7    | 47                     | 202.3     | 51                      | 0.92      |
| 256 KB       | 20           | 221.8    | 55                     | 233.5     | 58                      | 0.95      |
| 1 MB         | 1            | 32.9     | 33                     | 54.0      | 54                      | 0.61      |
| 1 MB         | 5            | 84.7     | 85                     | 92.0      | 92                      | 0.92      |
| 1 MB         | 10           | 132.0    | 132                    | 133.0     | 133                     | 0.99      |
| 1 MB         | 15           | 156.4    | 156                    | 156.1     | 156                     | 1.00      |
| 1 MB         | 20           | 188.3    | 188                    | 176.4     | 176                     | 1.07      |
| 16 MB        | 1            | 13.3     | 212                    | 5.6       | 90                      | 2.36      |
| 16 MB        | 5            | 32.9     | 526                    | 22.6      | 361                     | 1.46      |
| 16 MB        | 10           | 46.1     | 738                    | 24.7      | 396                     | 1.86      |
| 16 MB        | 15           | 52.6     | 842                    | 23.7      | 379                     | 2.22      |
| 16 MB        | 20           | 58.8     | 940                    | 23.6      | 378                     | 2.49      |
| 256 MB       | 1            | 1.6      | 421                    | 0.5       | 134                     | 3.14      |
| 256 MB       | 5            | 4.4      | 1114                   | 1.2       | 295                     | 3.78      |
| 256 MB       | 10           | 6.1      | 1570                   | 1.5       | 392                     | 4.01      |
| 256 MB       | 15           | 6.2      | 1578                   | 1.5       | 389                     | 4.06      |
| 256 MB       | 20           | 6.0      | 1544                   | 1.4       | 366                     | 4.22      |
| 50 GB        | 5            | 0.01     | 514                    | 0.0039    | 198                     | 2.60      |


Notes:

* Since auth server is single instance per node, it will not automatically scale
  with increasing number of s3server instances.  Thus, separate POC is needed
  for auth server RPS research.  Results here are only applicable to s3server
  instances.
* `R/W ratio` is `read_throughput` divided by `write_throughput`, i.e. how much
  faster we can read than we can write.

Conclusions from the test results on READ:

* With object sizes up to 256KB, RPS is over 200.  With 20 instances, this gives
  4k RPS per node, as required by DR.  We are thinking of 30 instances per node, which
  will give 6k RPS, so we should be good from C++ perspective.
  * Also, growth curve suggests that s3server can take in more than 20 clients,
    and RPS will continue to grow (i.e. there is still some resource to be
    utilized).
  * On the other hand, this is full fake, with no storage.  Adding storage will
    add overhead, and will reduce RPS.
* Throughput -- 10+ clients on 256 MB objects show throughput 1.5 GB/s with
  single s3 instance.  This is more than enough with our plan of having 20+
  instances.
  * This shows that data path is pretty good in C++ code, with single instance
    delivering half of the DR level on large objects.
* Note the disbalance: single instance is capable of delivering half of the
  GB/s, but only 1/20th of RPS.  This needs to be analyzed.
* On 16MB objects and 20 clients we get 940 MB/s.  Still very good, at 20
  instances it is 19GB/s, which is more than enough.
* So C++ code is good at throughput, but not so good at RPS.
* 5 clients test case shows throughput growth with objects of sizes 1 KB to 256 MB.
  However 50 GB throughput 2 times worse than 256 MB which means s3server is better
  optimized for medium sized objects. Dynamic memory tuning for requests could help
  to improve huge objects throughput.
* Read throughput consistently grows with object size, and seems to have reached
  the limit of 1.5 GB/s at 256 MB (not confirmed though, as we have not tried
  the next size).


Conclusions on WRITE:

* Write throughput seems to have reached its max of ~400 MB/s on 16 MB objects.
  Next tested object size 256 MB did not show any improvement in the throughput.
* There is no 100% correlation between read and write throughput -- in some
  cases write is faster, in some cases read is faster.
  * But there is a trend: write seen faster only on small objects.
  * Also, write throughput tops at 16 MB, while read keeps growing, and so on
    256 MB, read is 4 times faster than write (while on 16 MB it was only
    1.5-2.5 times faster).