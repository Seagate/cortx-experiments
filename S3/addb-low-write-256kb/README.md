# ADDB analysis of bottlenecks on low write throughput for small objects (256 KB)

One of problems identified in [EOS-16575](https://jts.seagate.com/browse/EOS-16575)
was stack is not able to deliver expected throughput for write of 256 KB objects.
Even for the "best case workload", we are more than 40 times slower than DR.

Contents:

- [ADDB analysis of bottlenecks on low write throughput for small objects (256 KB)](#addb-analysis-of-bottlenecks-on-low-write-throughput-for-small-objects-256-kb)
  - [Corresponding Jira Ticket](#corresponding-jira-ticket)
  - [Objectives](#objectives)
  - [Previous tests](#previous-tests)
  - [Test description](#test-description)
    - [Branches and repos](#branches-and-repos)
    - [Workload](#workload)
  - [Results](#results)
  - [GNUPlot](#gnuplot)
  - [Analysis](#analysis)
    - [Brief phases description](#brief-phases-description)
  - [Summary](#summary)

## Corresponding Jira Ticket

[EOS-17395](https://jts.seagate.com/browse/EOS-17395)

## Objectives

Run ADDB analysis and identify bottlenecks and possible improvements.

## Previous tests

- [EOS-16575: S3 POC on R2 HW - measure all perf metrics as they are now](https://jts.seagate.com/browse/EOS-16575)
- [Summary](https://github.com/Seagate/cortx-experiments/tree/main/S3/initial-perf-test-on-R2#throughput-for-object-size-256-kb)
- [Details](https://github.com/Seagate/cortx-experiments/blob/main/S3/initial-perf-test-on-R2/raw-test-results.md#2-256k-throughput-128-512-sessions)

## Test description

### Branches and repos

- Hare:
  - repo: [https://github.com/Seagate/cortx-hare.git](https://github.com/Seagate/cortx-hare.git)
  - branch: main

- Motr:
  - repo: [https://github.com/dsurnin/cortx-motr.git](https://github.com/dsurnin/cortx-motr.git)
  - branch: test-ext-addb-size-for-client

- S3:
  - repo: [https://github.com/Seagate/cortx-s3server.git](https://github.com/Seagate/cortx-s3server.git)
  - branch: main

### Workload

[256 KB throughput](./workload.yaml)

## Results

[Workload log file](./workload.log)
[CSV report](./small256kbrepnw.csv)
[Histogram](./hist-256kb-nw-detailed.png)
[m0play.db](root@sm14-r24.pun.seagate.com:/var/log/eos-17395/small256kb_nw/m0play.db)

## GNUPlot

Resulting [m0play.db](root@sm14-r24.pun.seagate.com:/var/log/eos-17395/small256kb_nw/m0play.db) database
it about 12GB in size. As a result it takes time to process and build single timeline. Also python
plotting tool is rather slow on dev vm. To avoid these limitation each timeline were processed once
and its data were dumped to ".dat" file in GNUPlot format and farther processing were done with help of GNUPlot.

Resulting ".dat" files are stored in [**raw-data**](./raw-data/) directory together with corresponding
timeline images in ".png" format.

[graph.gp](./graph.gp) is a command file for GNUPlot to draw timeline. It was tested on

- Linux: GNUPlot version 4.6 patchlevel 2
- Windows 10: GNUPlot version 5.4 patchlevel 1

Following command generates PNG image and opens window with timeline graph.
The graph could be moved, zoomed in/out, etc.

```
$ gnuplot -e "datafile='./raw-data/start_max.dat'" ./graph.gp
```

If interactive graph window is not required it could be disabled by commenting lines
from second terminal initialization to the end of the file.

## Analysis

Each PutObject request contains following phases

- START
- AUTH_CLNT_CONSTRUCT
- S3Action::load_metadata
- S3Action::set_authorization_meta
- S3Action::check_authorization
- AUTH_CLNT_CHK_AUTHZ
- AUTH_OP_CTX_CONSTRUCT
- AUTH_OP_CTX_NEW_CONN
- AUTH_CLNT_EXEC_AUTH_CONN
- AUTH_OP_ON_EVENT_CONNECTED
- AUTH_OP_ON_WRITE
- AUTH_OP_ON_HEADERS_READ
- AUTH_OP_ON_AUTHZ_RESP
- AUTH_CLNT_CHK_AUTHZ_SUCC
- S3PutObjectAction::validate_put_request
- S3PutObjectAction::create_object
- S3PutObjectAction::initiate_data_streaming
- S3PutObjectAction::save_metadata
- S3PutObjectAction::send_response_to_s3_client
- S3PutObjectAction::remove_new_oid_probable_record
- COMPLETE
- AUTH_CLNT_DESTRUCT
- AUTH_OP_CTX_DESTRUCT

For more details check [Histogram](./hist-256kb-nw-detailed.png).

For timeline processing for each state two requests were chosen - 1st corresponding to phase's max duration
and 2nd corresponding to phase's avg duration.

### Brief phases description

| Name                                       | Phase                                                                                              | Details                                                                                             | Impact                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|--------------------------------------------|----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| START_avg.dat.png                          |                                                                                                    | Avg 0.001 PID 97011, ID 7391                                                                        | OK. Short as it should be                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| START_max.dat.png                          |                                                                                                    | Max 0.18 PID 320252, ID 322                                                                         | OK. Still short. Analysis of the diff comparing with Avg is not a first priority task                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|                                            | AUTH_CLNT_CONSTRUCT to S3Action::load_metadata                                                     | Prepares client for AuthServer communications. Does not contain any operations outside the s3server |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| AUTH_CLNT_CONSTRUCT_avg.dat.png            |                                                                                                    | Avg 0.33 PID 320207 ID 3040                                                                         | OK                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| AUTH_CLNT_CONSTRUCT_max.dat.png            |                                                                                                    | Max 845.11 PID 296585 ID 2699                                                                       | Timeline is not detailed enough, requires src analysis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|                                            | S3Action::load_metadata to S3Action::set_authorization_meta                                        | Obtains data from KVS. Consists of 3 mero dix ops.                                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| load_metadata_avg.dat.png                  |                                                                                                    | Avg 197.53 PID 101094 ID 186                                                                        | 3 dix reqs: 1st and 2nd very short; 3rd 10 times longer;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| load_metadata_max.dat.png                  |                                                                                                    | Max 2647.81 PID 320252 ID 8421                                                                      | 3 dix reqs: 1st VERY long; 2nd 10 times shorter; 3rd VERY short;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|                                            | S3Action::set_authorization_meta to S3Action::check_authorization                                  | loads data from kvs responses to internal structs                                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| set_authorization_meta_avg.dat.png         |                                                                                                    | Avg 0.0 PID 296546 ID 166                                                                           | ok                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| set_authorization_meta_max.dat.png         |                                                                                                    | Max 0.51 PID 320161 ID 5729                                                                         | ok but probably should be checked since there are no any ext ops. not a first priority                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|                                            | S3Action::check_authorization to S3PutObjectAction::validate_put_request                           | sends data to AuthServer for authorization                                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| check_authorization_avg.dat.png            |                                                                                                    | Avg 1.67 PID 322414 ID 200                                                                          | ok                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| check_authorization_max.dat.png            |                                                                                                    | Max 673.98 PID 323200 ID 5792                                                                       | network communication between s3 and authserver takes all the phase time<br />S3Action::check_authorization - 0.000176%<br />AUTH_CLNT_CHK_AUTHZ - 0.00318%<br />AUTH_OP_CTX_CONSTRUCT - 0.000437%A<br />UTH_OP_CTX_NEW_CONN - 0.017116%<br />AUTH_CLNT_EXEC_AUTH_CONN - 0.001478%<br />AUTH_OP_ON_EVENT_CONNECTED - 0.002165%<br />AUTH_OP_ON_WRITE - 99.97065%<br />AUTH_OP_ON_HEADERS_READ - 0.00069%<br />AUTH_OP_ON_AUTHZ_RESP - 0.006783%<br />AUTH_CLNT_CHK_AUTHZ_SUCC - 0.000183%<br /><br />similar measurements of network activity should be done on AuthServer side |
|                                            | S3PutObjectAction::validate_put_request to S3PutObjectAction::create_object                        | check content of request's headers, aws restrictions, etc. no external calls.                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| validate_put_request_avg.dat.png           |                                                                                                    | Avg 0.02 PID 98320 ID 286                                                                           | ok                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| validate_put_request_max.dat.png           |                                                                                                    | Max 48.47 PID 96775 ID 7898                                                                         | too long for internal op only. need to research src                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|                                            | S3PutObjectAction::create_object to S3PutObjectAction::initiate_data_streaming                     | creates object in mero store. consists from cob req and probable-delete KVS index                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| create_object_avg.dat.png                  |                                                                                                    | Avg 545.09 PID 323783 ID 285                                                                        | cob and dix almost equal; no significant gaps between dix and next op;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| create_object_max.dat.png                  |                                                                                                    | Max 6684.75 PID 97943 ID 7389                                                                       | short cob; very long dix;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|                                            | S3PutObjectAction::initiate_data_streaming to S3PutObjectAction::save_metadata                     | actual storing obj data to mero store. consists of number of ioo reqs                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| initiate_data_streaming_avg.dat.png        |                                                                                                    | Avg 244.44 PID 296745 ID 4786                                                                       | ok - almost equal to the size of the single ioo req;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| initiate_data_streaming_max.dat.png        |                                                                                                    | Max 1631.5 PID 96963 ID 2644                                                                        | ok - almost equal to the size of the single ioo req; requires additional mero level research                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|                                            | S3PutObjectAction::save_metadata to S3PutObjectAction::send_response_to_s3_client                  | stires info about obj in KVS. consists of 2 mero dix reqs.                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| save_metadata_max.dat.png                  |                                                                                                    | Max 2265.07 PID 97297 ID 2420                                                                       | equal to the length of 2 dix reqs; dix2 is 2 time longer than dix1; requires additional mero level research                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| save_metadata_avg.dat.png                  |                                                                                                    | Avg 341.46 PID 296745 ID 173                                                                        | equal to the length of 2 dix reqs; dix1 is short; dix2 is 4 time longer than dix1; requires additional mero level research                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|                                            | S3PutObjectAction::send_response_to_s3_client to S3PutObjectAction::remove_new_oid_probable_record | prepares response and sends it to client                                                            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| send_response_to_s3_client_avg.dat.png     |                                                                                                    | Avg 0.17 PID 321773 ID 3148                                                                         | ok                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| send_response_to_s3_client_max.dat.png     |                                                                                                    | Max 657.65 PID 296826 ID 6390                                                                       | there are no any external ops - such a long time should be checked; send_response is complex operation, includes mutex and chunked event buffer modifications;                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                            | S3PutObjectAction::remove_new_oid_probable_record to COMPLETE                                      | remove temp entry from probable delete index. single KVS op. 1 mero dix op.                         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| remove_new_oid_probable_record_avg.dat.png |                                                                                                    | Avg 417.72 PID 297378 ID 6797                                                                       | single dix req; no gap;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| remove_new_oid_probable_record_max.dat.png |                                                                                                    | Max 6377.61 PID 97943 ID 7372                                                                       | single dix req; requires additional mero level research and s3server src                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

## Notes from S3/Motr discussion:

* Further steps: Use queues tool (Max fixed it).  See which stages are most filled.
* Motr: DIX is blocked on TX close operation.
* Try: POC with commented out probable delete index operations.  See how big the improvement is.
* Issue with BG delete not working, and probable-delete index growing.  May
  affect tests.  (Maybe add S3 flag to skip probable-delete operations, or
  new S3 API to re-create probable-delete index.)
* Not seeing gaps between Motr ops -- means there's no visible lock-ups in S3 code.
* Observed only two instances of long "gaps":
  * on auth server request
  * send resp to client
  * Both are related to network IO.
  * Future: when analyzing "tails", this must be looked into.
* Future: Need ADDB probes on every async step.  This will help in profiling, as we'll be able to build histograms for every step.
  * Now, for example, load metadata includes 3 motr op -- no easy way to profile them individually.

## Summary

- There are no any significant gaps between mero ops and s3
- The most significant gaps inside s3 are seen on network io like:
  - AuthServer communication - waiting to send/receive data
  - RequestObject::send_response - complex func, contains mutex and several event buffers ops
- The number of addb points should be increased in s3 code
- Need timelines for several avg requests to compare
  - requests that have total avg duration
  - requests that have each phase's duration close to phase's avg duration
- Need a diagram of requests' queues - the number of requests in particular state during the time
- Need to check with mero team if probable delete index could be removed now

Conclusion: Additional research with help of mero is required
