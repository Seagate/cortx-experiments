
Measure basic performance metrics as is on current version on R2 HW
===================================================================

Contents

- [Measure basic performance metrics as is on current version on R2 HW](#measure-basic-performance-metrics-as-is-on-current-version-on-r2-hw)
- [Goal of the POC](#goal-of-the-poc)
- [Environment details](#environment-details)
- [POC results - Summary](#poc-results---summary)
  - [Metrics summary](#metrics-summary)
  - [Follow-up POCs needed](#follow-up-pocs-needed)
- [POC results - Details](#poc-results---details)
  - [Throughput](#throughput)
    - [Throughput for object size 256 KB](#throughput-for-object-size-256-kb)
    - [Throughput for object size 16 MB](#throughput-for-object-size-16-mb)
    - [Write performance on small objects](#write-performance-on-small-objects)
  - [TTFB (time to first byte) and RPS (requests per second)](#ttfb-time-to-first-byte-and-rps-requests-per-second)
    - [TTFB/RPS, object size 100 bytes](#ttfbrps-object-size-100-bytes)
    - [TTFB/RPS, object size 1 KB](#ttfbrps-object-size-1-kb)
    - [TTFB/RPS, object size 16 KB](#ttfbrps-object-size-16-kb)
    - [TTFB/RPS, object size 100 KB](#ttfbrps-object-size-100-kb)
    - [TTFB/RPS, object size 256 KB](#ttfbrps-object-size-256-kb)
    - [TTFB/RPS, object size 1 MB](#ttfbrps-object-size-1-mb)
    - [TTFB/RPS, object size 5 MB](#ttfbrps-object-size-5-mb)
    - [TTFB/RPS, object size 16 MB](#ttfbrps-object-size-16-mb)
    - [TTFB/RPS, object size 64 MB](#ttfbrps-object-size-64-mb)
    - [TTFB/RPS, object size 128 MB](#ttfbrps-object-size-128-mb)
  - [Single stream read (based on TTFB test run)](#single-stream-read-based-on-ttfb-test-run)


Goal of the POC
===============

Measure current performance characteristics as they are on R2 with recent build
-- to have a reference point.

Specific metrics to assess:

* Throughput at 16M and 256K objects.
* TTFB at various object sizes.
* RPS (requests per second) -- for small objects.
* Max possible number of parallel sessions.


Environment details
===================

* 3 server node, 3 enclosures, fully stuffed (all disks).  R2-spec'd.
* S3 load is generated from stand-alone client node.  Using s3bench internal
  facility for load distribution (no external load balancers).
* IMPORTANT NOTE -- this test is done on plain HTTP, no SSL.


POC results - Summary
======================

Metrics summary
---------------

Basic metrics (DR):

* Throughput:
  * 256 KB:
    * Write -- 20 MB/s per node (achieved at 384 parallel sessions).
    * Read -- 109 MB/s per node (achieved at 128 parallel sessions).
  * 16 MB:
    * Write -- 530 MB/s per node (achieved at 512 parallel sessions).
    * Read -- 2992 MB/s per node (achieved at 512 parallel sessions).
* TTFB (time to first byte), 99th percentile, measured on object sizes 100 bytes
  -- 128 MB:
  * 1 parallel session -- 27-118 ms.
  * 16 parallel sessions -- 123-358 ms.  (96 ms at 1 MB object size, not sure
    it's valid data point.)
  * 32 sessions -- 126-678 ms.
  * 64 sessions -- 120-750 ms.
  * 128 sessions -- 173-1770 ms.
  * 256 sessions -- 256-3960 ms.
  * 384 sessions -- 566-7417 ms.
  * 512 sessions -- 736-7494 ms.
  * NOTE: specific object sizes tested: 100 B, 1 KB, 16 KB, 100 KB, 256 KB, 1
    MB, 16 MB, 64 MB, 128 MB.
* RPS (requests per second):
  * on 128-256 sessions, on objects of size up to 1 MB:
    * 400-500 RPS per node.
* Max parallel sessions:
  * IO is stable up to 170 sessions per node.
  * IO has failed in test with 300 sessions per node.

Additional metrics:

* Single stream read:
  * 256 KB -- 6.5 MB/s, 26 objects per second
  * 16 MB -- 224 MB/s, 14 objects per second
* Single stream for tiny object (100 bytes):
  * Read 14 ms per object.
  * Write 1.6 seconds (1600 ms) per object.


Follow-up POCs needed
---------------------

* What is the root cause of the error we get with 900+ sessions (256 KB).
* ADDB analysis of bottlenecks on low write throughput for small objects (256 KB).
* ADDB analysis of bottlenecks on low read throughput for small objects (256 KB).
* ADDB analysis of bottlenecks on low write throughput for 16 MB objects.
* ADDB analysis of single-stream write -- why it is so slow?
* Analyze TTFB "outliers" -- requests which show significantly higher TTFB than
  average.  (See if there are multiple peaks at the histogram; review individual
  requests one by one.)
* Use ADDB queues analysis to see why RPS is degrading on small objects (100 B)
  after 128/256 sessions.
* Analyze why such big difference in operation duration for 1 KB vs 16 KB (see
  TTFB test for 16 KB for detailed description).
* Run "modified" S3 with first read 1M for large objects, and compare TTFB with
  measurements done in this test.  See if that fix resolves "extremely huge"
  TTFBs for large objects or not (i.e. is it the only reason or not).  Check
  ADDB timelines to see the problem from another angle.
* ADDB analysis why TTFB for large objects varies this much with growing number
  of sessions.


POC results - Details
======================

Full logs:

* [baseline performance test run log](s3-perf-test-log-2021-01-27_04-23-09.txt).
* [s3bench runs logs](raw-test-results.md).
* [CSV report](results.csv)


Throughput
----------

### Throughput for object size 256 KB

Measurements below are showing totals for cluster (not per-node).

| `numClients` | write (MB/s) | read (MB/s) | write test length (s) | read test length (s) |
| -----------: | -----------: | ----------: | --------------------: | -------------------: |
| 32           | 6            | 133         | 374                   | 260                  |
| 64           | 12           | 223         | 186                   | 155                  |
| 80           | 15           | 267         | 158                   | 129                  |
| 100          | 17           | 261         | 133                   | 132                  |
| 128          | 22           | 326         | 103                   | 105                  |
| 256          | 48           | 232         | 48                    | 149                  |
| 384          | 61           | 280         | 38                    | 123                  |
| 512          | 56           | 197         | 41                    | 176                  |
| 900          | - FAILED -   | - FAILED -  | - FAILED -            | - FAILED -           |

* Write peaks at around 384 sessions, which gives 61 MB/s (20 MB/s per node).
* Read peaks at around 128 sessions, which gives 326 MB/s (109 MB/s per node).


### Throughput for object size 16 MB

| `numClients` | write (MB/s) | read (MB/s) | write test length (s) | read test length (s) |
| -----------: | -----------: | ----------: | --------------------: | -------------------: |
| 32           | 356          | 4048        | 115                   | 51                   |
| 64           | 758          | 5503        | 95                    | 104                  |
| 80           | 1097         | 5995        | 82                    | 135                  |
| 100          | 1350         | 6486        | 83                    | 121                  |
| 128          | 1482         | 6759        | 111                   | 145                  |
| 256          | 1352         | 8440        | 121                   | 116                  |
| 384          | 1502         | 8822        | 115                   | 117                  |
| 512          | 1592         | 8975        | 103                   | 110                  |

* Write grows steadily, but we can see it is flattening after 384 sessions (it
  could have grown a bit more after 512, but it was not tested with 16M and it
  was failing with smaller objects).
  * Write is 1.6 GB/s (at 512 sessions).
* Read also grows steadily and also flattens on higher session counts.
  * Read is 9 GB/s (at 512 sessions).


### Write performance on small objects

This was not listed as a metric in original test plan, but it is so much
outstanding that it deserves separate note.

Observed during TTFB test:
	
* test runs write then read,
* objects of size 100 bytes,
* one by one (no parallelism),
* 256 objects.

Notes:

* No optimizations, code as is in stable branches.

Observations:

* write -- takes 400 seconds total (1.6 seconds per object).
* read -- takes 3.5 seconds total (14ms per object).

Difference is two orders of magnitude.  Writes are 100 times slower than reads.


## TTFB (time to first byte) and RPS (requests per second)

### TTFB/RPS, object size 100 bytes

Metrics in TTFB/RPS tests:

* `numClients` -- number of parallel sessions, sending simultaneous S3 API requests.
* `TTFB avg (ms)` -- average time to first byte in milliseconds.
* `TTFB 99th-ile (ms)` -- 99-th percentile of TTFB (i.e., 99% of all the request
  demonstrate TTFB less than this value).
* `RPS` -- requests per second (total value per cluster of 3 nodes).  From S3
  protocol perspective, this is the same as IOPS.
* `read test length (s)` -- total duration of the "read" phase in this test, in seconds.


| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 14            | 27                 | 73   | 141                  |
| 16           | 47            | 162                | 500  | 85                   |
| 32           | 41            | 140                | 785  | 65                   |
| 64           | 53            | 124                | 1208 | 106                  |
| 128          | 89            | 179                | 1446 | 106                  |
| 256          | 169           | 403                | 1510 | 102                  |
| 384          | 360           | 587                | 1065 | 146                  |
| 512          | 743           | 1163               | 688  | 223                  |

Notes:

* TTFB grows rapidly with number of sessions, and 99th percentile is only
  satisfying DR when testing below 16 sessions.
* TTFB 99th percentile is 2-3 times worse than average.  Way too many samples
  are out of 150ms (only 1% is allowed).
* Best RPS (request per second) is observed on 256 sessions, and is 1510
  requests per second total, or 503 requests per second per node.


### TTFB/RPS, object size 1 KB

| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 14            | 26                 | 73   | 141                  |
| 16           | 38            | 218                | 424  | 91                   |
| 32           | 42            | 137                | 751  | 68                   |
| 64           | 55            | 128                | 1167 | 110                  |
| 128          | 90            | 196                | 1422 | 108                  |
| 256          | 221           | 405                | 1155 | 133                  |
| 384          | 346           | 717                | 1108 | 140                  |
| 512          | 394           | 736                | 1297 | 118                  |

Notes:

* Used the same count of samples to 100b, and observe very similar TTFB.
* Highest RPS is 1422 (with 128 sessions).


### TTFB/RPS, object size 16 KB

| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 15            | 41                 | 18   | 561                  |
| 16           | 28            | 256                | 239  | 161                  |
| 32           | 35            | 126                | 442  | 116                  |
| 64           | 46            | 120                | 789  | 162                  |
| 128          | 69            | 181                | 1212 | 128                  |
| 256          | 151           | 345                | 1370 | 112                  |
| 384          | 296           | 609                | 1155 | 135                  |
| 512          | 656           | 1132               | 738  | 208                  |

Notes:

* Compare full output of TTFB test (in
  [raw-test-results.md](raw-test-results.md)) for 1KB and 16KB.  TTFB is almost
  equal (14 vs 15 ms), while average single operation duration changes
  dramatically (14ms for 1KB and 55ms for 16KB) -- 3.5x times increase.
  Throughput is still negligible 285KB/s, should not be the reason for this
  slowdown.
* Most of tests (except 1 session and 512 sessions) show better average TTFB
  than 1KB and 100B.  Most probably -- because IOPS are lower, so less load on
  metadata path (KVS, Auth), and thus faster response.
* Ratio of 99th-ile to TTFB average is getting worse.  It is now almost 3, and
  in one case it is as high as 9 -- see 16 sessions, average is 28, 99th-ile is
  256, 9 times higher).


### TTFB/RPS, object size 100 KB

| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 14            | 31                 | 39   | 265                  |
| 16           | 27            | 173                | 274  | 140                  |
| 32           | 33            | 126                | 474  | 108                  |
| 64           | 47            | 130                | 776  | 165                  |
| 128          | 72            | 173                | 1193 | 129                  |
| 256          | 197           | 419                | 1103 | 139                  |
| 384          | 313           | 682                | 1099 | 142                  |
| 512          | 581           | 1047               | 830  | 185                  |

Notes:

* TTFB is approximately on same levels.
* 16 sessions test again shows higher 99th-ile (not as high as in 16 KB though).
* RPS is getting lower and lower with every size increase.


### TTFB/RPS, object size 256 KB

| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 15            | 39                 | 26   | 392                  |
| 16           | 26            | 123                | 324  | 119                  |
| 32           | 36            | 138                | 521  | 98                   |
| 64           | 47            | 130                | 876  | 146                  |
| 128          | 78            | 173                | 1230 | 125                  |
| 256          | 140           | 256                | 1530 | 100                  |
| 384          | 378           | 701                | 948  | 164                  |
| 512          | 528           | 801                | 923  | 167                  |

No major difference to previous results.


### TTFB/RPS, object size 1 MB

| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 18            | 59                 | 20   | 505                  |
| 16           | 24            | 96                 | 303  | 127                  |
| 32           | 36            | 129                | 501  | 102                  |
| 64           | 52            | 142                | 807  | 159                  |
| 128          | 78            | 213                | 1199 | 128                  |
| 256          | 213           | 542                | 1059 | 145                  |
| 384          | 248           | 566                | 1386 | 112                  |
| 512          | 479           | 887                | 1007 | 153                  |

Notes:

* All in all, no major differences in TTFB between measured object sizes up till 256KB.
* Variations on RPS are higher between these object sizes, but still close
  (1200-1500 RPS).


### TTFB/RPS, object size 5 MB

| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 25            | 52                 | 17   | 589                  |
| 16           | 35            | 133                | 255  | 151                  |
| 32           | 51            | 172                | 426  | 120                  |
| 64           | 76            | 190                | 624  | 205                  |
| 128          | 117           | 374                | 893  | 172                  |
| 256          | 216           | 511                | 1051 | 146                  |
| 384          | 383           | 826                | 934  | 167                  |
| 512          | 496           | 1055               | 972  | 158                  |

Notes:

* Now TTFB starts growing with each object size increase (especially noticeable
  on small number of sessions).
* RPS goes down as well.
* TTFB average to 99th-ile is still within 2-3.


### TTFB/RPS, object size 16 MB

| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 37            | 67                 | 14   | 91                   |
| 16           | 49            | 133                | 228  | 29                   |
| 32           | 95            | 578                | 248  | 54                   |
| 64           | 146           | 471                | 377  | 81                   |
| 128          | 187           | 784                | 371  | 83                   |
| 256          | 524           | 2410               | 424  | 121                  |
| 384          | 621           | 1409               | 542  | 96                   |
| 512          | 896           | 1634               | 538  | 95                   |

Notes:

* TTFB keeps growing.
* Significant drop in RPS -- obviously due to object size.  Now the raw data
  throughput starts affecting RPS and becomes a bottleneck here.  (On the other
  hand, low RPS is not a problem per se for 16 MB, high RPS is only required for
  small objects.)
* Significant increase in TTFB average to 99th-ile ratio.  4 of 8 tests have
  this ratio above 3.  This may indicate that outliers are caused by IO.


### TTFB/RPS, object size 64 MB

| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 74            | 118                | 8    | 41                   |
| 16           | 143           | 352                | 59   | 76                   |
| 32           | 187           | 493                | 77   | 116                  |
| 64           | 211           | 620                | 92   | 277                  |
| 128          | 367           | 1051               | 110  | 232                  |
| 256          | 660           | 1956               | 114  | 225                  |
| 384          | 2286          | 5183               | 88   | 307                  |
| 512          | 3305          | 7494               | 79   | 323                  |

Notes:

* Even bigger increase in TTFB.
  * Reason -- at large objects, first read operation which comes to Motr from S3
    is going to read 32 MB. On 16M objects it was reading 16M (entire object), for
    64MB it was reading 32M, this is one reason.
  * Not sure if there are other reasons.


### TTFB/RPS, object size 128 MB

| `numClients` | TTFB avg (ms) | TTFB 99th-ile (ms) | RPS  | read test length (s) |
| -----------: | ------------: | -----------------: | ---: | -------------------: |
| 1            | 73            | 109                | 4    | 156                  |
| 16           | 146           | 358                | 31   | 72                   |
| 32           | 202           | 552                | 42   | 106                  |
| 64           | 271           | 754                | 51   | 100                  |
| 128          | 382           | 1770               | 45   | 227                  |
| 256          | 1617          | 3958               | 38   | 269                  |
| 384          | 2444          | 7417               | 39   | 293                  |
| 512          | 2830          | 6343               | 47   | 216                  |

Notes:

* Slight increase in TTFB on 1-128 clients, and huge jump on 256.  Maybe
  something temporary.


## Single stream read (based on TTFB test run)

As a side-effect of TTFB tests (see above), we have a summary on "single stream read", i.e. read when only 1 single parallel session is connected to S3.

| size (MB)   | size         | `numClients` | read throughput (MB/s) | IOPS | read test length (s) |
| ----------- | -----------: | -----------: | ---------------------- | ---: | -------------------: |
| 0.000095    | 100 B        | 1            | 0.006935               | 73   | 141                  |
| 0.00098     | 1 KB         | 1            | 0.07154                | 73   | 141                  |
| 0.016       | 16 KB        | 1            | 0.288                  | 18   | 561                  |
| 0.098       | 100 KB       | 1            | 3.822                  | 39   | 265                  |
| 0.25        | 256 KB       | 1            | 6.5                    | 26   | 392                  |
| 1           | 1 MB         | 1            | 20                     | 20   | 505                  |
| 5           | 5 MB         | 1            | 85                     | 17   | 589                  |
| 16          | 16 MB        | 1            | 224                    | 14   | 91                   |
| 64          | 64 MB        | 1            | 512                    | 8    | 41                   |
| 128         | 128 MB       | 1            | 512                    | 4    | 156                  |
