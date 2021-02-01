
# 1. Raw s3bench output

Contents:

- [1. Raw s3bench output](#1-raw-s3bench-output)
- [2. 256k throughput, 128-512 sessions](#2-256k-throughput-128-512-sessions)
  - [2.1. PerfLine job YAML](#21-perfline-job-yaml)
  - [2.2. 128 sessions](#22-128-sessions)
  - [2.3. 256 sessions](#23-256-sessions)
  - [2.4. 384 sessions](#24-384-sessions)
  - [2.5. 512 sessions](#25-512-sessions)
- [3. 256k throughput, 32-100 sessions](#3-256k-throughput-32-100-sessions)
  - [3.1. PerfLine job YAML](#31-perfline-job-yaml)
  - [3.2. 100 sessions](#32-100-sessions)
  - [3.3. 80 sessions](#33-80-sessions)
  - [3.4. 64 sessions](#34-64-sessions)
  - [3.5. 32 sessions](#35-32-sessions)
- [4. 16MB throughput, 128-512 sessions, 1 minute test](#4-16mb-throughput-128-512-sessions-1-minute-test)
  - [4.1. PerfLine job YAML](#41-perfline-job-yaml)
  - [4.2. 128 sessions](#42-128-sessions)
  - [4.3. 256 sessions](#43-256-sessions)
  - [4.4. 384 sessions](#44-384-sessions)
  - [4.5. 512 sessions](#45-512-sessions)
- [5. 16MB throughput, 128-512 sessions, 2 minutes test](#5-16mb-throughput-128-512-sessions-2-minutes-test)
  - [5.1. PerfLine job YAML](#51-perfline-job-yaml)
  - [5.2. 128 sessions](#52-128-sessions)
  - [5.3. 256 sessions](#53-256-sessions)
  - [5.4. 384 sessions](#54-384-sessions)
  - [5.5. 512 sessions](#55-512-sessions)
- [6. 16MB throughput, 32-100 sessions, 2 minutes test](#6-16mb-throughput-32-100-sessions-2-minutes-test)
  - [6.1. PerfLine job YAML](#61-perfline-job-yaml)
  - [6.2. 32 sessions](#62-32-sessions)
  - [6.3. 64 sessions](#63-64-sessions)
  - [6.4. 80 sessions](#64-80-sessions)
  - [6.5. 100 sessions](#65-100-sessions)
- [7. TTFB, 100b, 1-128 sessions - too short, ignore](#7-ttfb-100b-1-128-sessions---too-short-ignore)
  - [7.1. PerfLine job YAML](#71-perfline-job-yaml)
  - [7.2. 1 session -- to be ignored, too quick read phase (4sec)](#72-1-session----to-be-ignored-too-quick-read-phase-4sec)
- [8. TTFB, 100 bytes, 1-512 sessions - take 2](#8-ttfb-100-bytes-1-512-sessions---take-2)
  - [8.1. PerfLine job YAML](#81-perfline-job-yaml)
  - [8.2. 1 session](#82-1-session)
  - [8.3. 16 sessions](#83-16-sessions)
  - [8.4. 32 sessions](#84-32-sessions)
  - [8.5. 64 sessions](#85-64-sessions)
  - [8.6. 128 sessions](#86-128-sessions)
  - [8.7. 256 sessions](#87-256-sessions)
  - [8.8. 384 sessions](#88-384-sessions)
  - [8.9. 512 sessions](#89-512-sessions)
- [9. TTFB, 100 bytes, 900 sessions - FAILED](#9-ttfb-100-bytes-900-sessions---failed)
  - [9.1. PerfLine job YAML](#91-perfline-job-yaml)
  - [9.2. 900 sessions](#92-900-sessions)
- [10. TTFB, 1 KB, 1-512 sessions](#10-ttfb-1-kb-1-512-sessions)
  - [10.1. PerfLine job YAML](#101-perfline-job-yaml)
  - [10.2. 1 session](#102-1-session)
  - [10.3. 16 sessions](#103-16-sessions)
  - [10.4. 32 sessions](#104-32-sessions)
  - [10.5. 64 sessions](#105-64-sessions)
  - [10.6. 128 sessions](#106-128-sessions)
  - [10.7. 256 sessions](#107-256-sessions)
  - [10.8. 384 sessions](#108-384-sessions)
  - [10.9. 512 sessions](#109-512-sessions)
- [11. TTFB, 16 KB, 1-512 sessions](#11-ttfb-16-kb-1-512-sessions)
  - [11.1. PerfLine job YAML](#111-perfline-job-yaml)
  - [11.2. 1 session](#112-1-session)
  - [11.3. 16 sessions](#113-16-sessions)
  - [11.4. 32 sessions](#114-32-sessions)
  - [11.5. 64 sessions](#115-64-sessions)
  - [11.6. 128 sessions](#116-128-sessions)
  - [11.7. 256 sessions](#117-256-sessions)
  - [11.8. 384 sessions](#118-384-sessions)
  - [11.9. 512 sessions](#119-512-sessions)
- [12. TTFB, 100 KB, 1-512 sessions](#12-ttfb-100-kb-1-512-sessions)
  - [12.1. PerfLine job YAML](#121-perfline-job-yaml)
  - [12.2. 1 session](#122-1-session)
  - [12.3. 16 sessions](#123-16-sessions)
  - [12.4. 32 sessions](#124-32-sessions)
  - [12.5. 64 sessions](#125-64-sessions)
  - [12.6. 128 sessions](#126-128-sessions)
  - [12.7. 256 sessions](#127-256-sessions)
  - [12.8. 384 sessions](#128-384-sessions)
  - [12.9. 512 sessions](#129-512-sessions)
- [13. TTFB, 256 KB, 1-512 sessions](#13-ttfb-256-kb-1-512-sessions)
  - [13.1. PerfLine job YAML](#131-perfline-job-yaml)
  - [13.2. 1 session](#132-1-session)
  - [13.3. 16 sessions](#133-16-sessions)
  - [13.4. 32 sessions](#134-32-sessions)
  - [13.5. 64 sessions](#135-64-sessions)
  - [13.6. 128 sessions](#136-128-sessions)
  - [13.7. 256 sessions](#137-256-sessions)
  - [13.8. 384 sessions](#138-384-sessions)
  - [13.9. 512 sessions](#139-512-sessions)
- [14. TTFB, 1 MB, 1-512 sessions](#14-ttfb-1-mb-1-512-sessions)
  - [14.1. PerfLine job YAML](#141-perfline-job-yaml)
  - [14.2. 1 session](#142-1-session)
  - [14.3. 16 sessions](#143-16-sessions)
  - [14.4. 32 sessions](#144-32-sessions)
  - [14.5. 64 sessions](#145-64-sessions)
  - [14.6. 128 sessions](#146-128-sessions)
  - [14.7. 256 sessions](#147-256-sessions)
  - [14.8. 384 sessions](#148-384-sessions)
  - [14.9. 512 sessions](#149-512-sessions)
- [15. TTFB, 5 MB, 1-512 sessions](#15-ttfb-5-mb-1-512-sessions)
  - [15.1. PerfLine job YAML](#151-perfline-job-yaml)
  - [15.2. 1 session](#152-1-session)
  - [15.3. 16 sessions](#153-16-sessions)
  - [15.4. 32 sessions](#154-32-sessions)
  - [15.5. 64 sessions](#155-64-sessions)
  - [15.6. 128 sessions](#156-128-sessions)
  - [15.7. 256 sessions](#157-256-sessions)
  - [15.8. 384 sessions](#158-384-sessions)
  - [15.9. 512 sessions](#159-512-sessions)
- [16. TTFB, 16 MB, 1-512 sessions](#16-ttfb-16-mb-1-512-sessions)
  - [16.1. PerfLine job YAML](#161-perfline-job-yaml)
  - [16.2. 1 session](#162-1-session)
  - [16.3. 16 sessions](#163-16-sessions)
  - [16.4. 32 sessions](#164-32-sessions)
  - [16.5. 64 sessions](#165-64-sessions)
  - [16.6. 128 sessions](#166-128-sessions)
  - [16.7. 256 sessions](#167-256-sessions)
  - [16.8. 384 sessions](#168-384-sessions)
  - [16.9. 512 sessions](#169-512-sessions)
- [17. TTFB, 64 MB, 1-512 sessions](#17-ttfb-64-mb-1-512-sessions)
  - [17.1. PerfLine job YAML](#171-perfline-job-yaml)
  - [17.2. 1 session](#172-1-session)
  - [17.3. 16 sessions](#173-16-sessions)
  - [17.4. 32 sessions](#174-32-sessions)
  - [17.5. 64 sessions](#175-64-sessions)
  - [17.6. 128 sessions](#176-128-sessions)
  - [17.7. 256 sessions](#177-256-sessions)
  - [17.8. 384 sessions](#178-384-sessions)
  - [17.9. 512 sessions](#179-512-sessions)
- [18. TTFB, 128 MB, 1-512 sessions](#18-ttfb-128-mb-1-512-sessions)
  - [18.1. PerfLine job YAML](#181-perfline-job-yaml)
  - [18.2. 1 session](#182-1-session)
  - [18.3. 16 sessions](#183-16-sessions)
  - [18.4. 32 sessions](#184-32-sessions)
  - [18.5. 64 sessions](#185-64-sessions)
  - [18.6. 128 sessions](#186-128-sessions)
  - [18.7. 256 sessions](#187-256-sessions)
  - [18.8. 384 sessions](#188-384-sessions)
  - [18.9. 512 sessions](#189-512-sessions)
- [19. --template-- TTFB, 1 KB, 1-512 sessions](#19---template---ttfb-1-kb-1-512-sessions)
  - [19.1. PerfLine job YAML](#191-perfline-job-yaml)
  - [19.2. test 1](#192-test-1)

# 2. 256k throughput, 128-512 sessions

## 2.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 5
  batch_id: 256k-throughput-v2
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 9216 -c 128 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 9216 -c 256 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 9216 -c 384 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 9216 -c 512 -o 256Kb -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 2.2. 128 sessions

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 9216
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       9216
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    22.164
smc73-m02:     Duration Max:               2.353
smc73-m02:     Duration Avg:               1.434
smc73-m02:     Duration Min:               0.485
smc73-m02:     Ttfb Max:                   2.353
smc73-m02:     Ttfb Avg:                   1.434
smc73-m02:     Ttfb Min:                   0.485
smc73-m02:     Duration 90th-ile:          1.619
smc73-m02:     Duration 99th-ile:          1.908
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         103.951
smc73-m02:     Total Transferred (MB):     2304.000
smc73-m02:     Ttfb 90th-ile:              1.619
smc73-m02:     Ttfb 99th-ile:              1.908
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       138240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    326.755
smc73-m02:     Duration Max:               1.471
smc73-m02:     Duration Avg:               0.098
smc73-m02:     Duration Min:               0.011
smc73-m02:     Ttfb Max:                   1.430
smc73-m02:     Ttfb Avg:                   0.071
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.135
smc73-m02:     Duration 99th-ile:          0.206
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         105.767
smc73-m02:     Total Transferred (MB):     34560.000
smc73-m02:     Ttfb 90th-ile:              0.102
smc73-m02:     Ttfb 99th-ile:              0.172
```

## 2.3. 256 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 9216
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       9216
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    47.996
smc73-m02:     Duration Max:               5.760
smc73-m02:     Duration Avg:               1.291
smc73-m02:     Duration Min:               0.328
smc73-m02:     Ttfb Max:                   5.760
smc73-m02:     Ttfb Avg:                   1.291
smc73-m02:     Ttfb Min:                   0.328
smc73-m02:     Duration 90th-ile:          2.475
smc73-m02:     Duration 99th-ile:          3.620
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         48.004
smc73-m02:     Total Transferred (MB):     2304.000
smc73-m02:     Ttfb 90th-ile:              2.475
smc73-m02:     Ttfb 99th-ile:              3.620
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       138240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    232.147
smc73-m02:     Duration Max:               1.759
smc73-m02:     Duration Avg:               0.275
smc73-m02:     Duration Min:               0.021
smc73-m02:     Ttfb Max:                   1.719
smc73-m02:     Ttfb Avg:                   0.249
smc73-m02:     Ttfb Min:                   0.021
smc73-m02:     Duration 90th-ile:          0.335
smc73-m02:     Duration 99th-ile:          0.507
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         148.871
smc73-m02:     Total Transferred (MB):     34560.000
smc73-m02:     Ttfb 90th-ile:              0.303
smc73-m02:     Ttfb 99th-ile:              0.477
```

## 2.4. 384 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 9216
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       9216
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    61.196
smc73-m02:     Duration Max:               7.990
smc73-m02:     Duration Avg:               1.529
smc73-m02:     Duration Min:               0.420
smc73-m02:     Ttfb Max:                   7.990
smc73-m02:     Ttfb Avg:                   1.529
smc73-m02:     Ttfb Min:                   0.420
smc73-m02:     Duration 90th-ile:          2.737
smc73-m02:     Duration 99th-ile:          5.716
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         37.649
smc73-m02:     Total Transferred (MB):     2304.000
smc73-m02:     Ttfb 90th-ile:              2.737
smc73-m02:     Ttfb 99th-ile:              5.716
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       138240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    280.746
smc73-m02:     Duration Max:               1.629
smc73-m02:     Duration Avg:               0.342
smc73-m02:     Duration Min:               0.030
smc73-m02:     Ttfb Max:                   1.589
smc73-m02:     Ttfb Avg:                   0.315
smc73-m02:     Ttfb Min:                   0.030
smc73-m02:     Duration 90th-ile:          0.393
smc73-m02:     Duration 99th-ile:          0.577
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         123.101
smc73-m02:     Total Transferred (MB):     34560.000
smc73-m02:     Ttfb 90th-ile:              0.360
smc73-m02:     Ttfb 99th-ile:              0.547
```

## 2.5. 512 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 9216
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       9216
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    55.567
smc73-m02:     Duration Max:               15.613
smc73-m02:     Duration Avg:               2.244
smc73-m02:     Duration Min:               0.431
smc73-m02:     Ttfb Max:                   15.613
smc73-m02:     Ttfb Avg:                   2.244
smc73-m02:     Ttfb Min:                   0.431
smc73-m02:     Duration 90th-ile:          4.001
smc73-m02:     Duration 99th-ile:          12.870
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         41.463
smc73-m02:     Total Transferred (MB):     2304.000
smc73-m02:     Ttfb 90th-ile:              4.001
smc73-m02:     Ttfb 99th-ile:              12.870
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       138240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    196.692
smc73-m02:     Duration Max:               2.351
smc73-m02:     Duration Avg:               0.650
smc73-m02:     Duration Min:               0.032
smc73-m02:     Ttfb Max:                   2.350
smc73-m02:     Ttfb Avg:                   0.624
smc73-m02:     Ttfb Min:                   0.032
smc73-m02:     Duration 90th-ile:          0.741
smc73-m02:     Duration 99th-ile:          1.016
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         175.706
smc73-m02:     Total Transferred (MB):     34560.000
smc73-m02:     Ttfb 90th-ile:              0.713
smc73-m02:     Ttfb 99th-ile:              0.986
```


# 3. 256k throughput, 32-100 sessions

## 3.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 5
  batch_id: 256k-throughput-v3
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 9200 -c 100 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 9200 -c  80 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 9216 -c  64 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 9216 -c  32 -o 256Kb -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 3.2. 100 sessions

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 100
smc73-m02:     numSamples:                 9200
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       9200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    17.347
smc73-m02:     Duration Max:               2.266
smc73-m02:     Duration Avg:               1.433
smc73-m02:     Duration Min:               0.731
smc73-m02:     Ttfb Max:                   2.266
smc73-m02:     Ttfb Avg:                   1.433
smc73-m02:     Ttfb Min:                   0.731
smc73-m02:     Duration 90th-ile:          1.596
smc73-m02:     Duration 99th-ile:          1.999
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         132.591
smc73-m02:     Total Transferred (MB):     2300.000
smc73-m02:     Ttfb 90th-ile:              1.596
smc73-m02:     Ttfb 99th-ile:              1.999
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       138000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    261.979
smc73-m02:     Duration Max:               0.972
smc73-m02:     Duration Avg:               0.095
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   0.933
smc73-m02:     Ttfb Avg:                   0.069
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.133
smc73-m02:     Duration 99th-ile:          0.201
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         131.690
smc73-m02:     Total Transferred (MB):     34500.000
smc73-m02:     Ttfb 90th-ile:              0.101
smc73-m02:     Ttfb 99th-ile:              0.169
```

## 3.3. 80 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 80
smc73-m02:     numSamples:                 9200
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       9200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    14.533
smc73-m02:     Duration Max:               2.734
smc73-m02:     Duration Avg:               1.371
smc73-m02:     Duration Min:               0.605
smc73-m02:     Ttfb Max:                   2.734
smc73-m02:     Ttfb Avg:                   1.371
smc73-m02:     Ttfb Min:                   0.605
smc73-m02:     Duration 90th-ile:          1.594
smc73-m02:     Duration 99th-ile:          2.058
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         158.258
smc73-m02:     Total Transferred (MB):     2300.000
smc73-m02:     Ttfb 90th-ile:              1.594
smc73-m02:     Ttfb 99th-ile:              2.058
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       138000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    266.880
smc73-m02:     Duration Max:               1.184
smc73-m02:     Duration Avg:               0.075
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   1.145
smc73-m02:     Ttfb Avg:                   0.048
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.112
smc73-m02:     Duration 99th-ile:          0.160
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         129.271
smc73-m02:     Total Transferred (MB):     34500.000
smc73-m02:     Ttfb 90th-ile:              0.080
smc73-m02:     Ttfb 99th-ile:              0.126
```

## 3.4. 64 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 9216
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       9216
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    12.398
smc73-m02:     Duration Max:               2.514
smc73-m02:     Duration Avg:               1.284
smc73-m02:     Duration Min:               0.492
smc73-m02:     Ttfb Max:                   2.514
smc73-m02:     Ttfb Avg:                   1.284
smc73-m02:     Ttfb Min:                   0.492
smc73-m02:     Duration 90th-ile:          1.561
smc73-m02:     Duration 99th-ile:          1.775
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         185.841
smc73-m02:     Total Transferred (MB):     2304.000
smc73-m02:     Ttfb 90th-ile:              1.561
smc73-m02:     Ttfb 99th-ile:              1.775
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       138240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    222.877
smc73-m02:     Duration Max:               1.328
smc73-m02:     Duration Avg:               0.072
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   1.288
smc73-m02:     Ttfb Avg:                   0.045
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.110
smc73-m02:     Duration 99th-ile:          0.155
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         155.063
smc73-m02:     Total Transferred (MB):     34560.000
smc73-m02:     Ttfb 90th-ile:              0.079
smc73-m02:     Ttfb 99th-ile:              0.122
```

## 3.5. 32 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 9216
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       9216
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6.160
smc73-m02:     Duration Max:               1.949
smc73-m02:     Duration Avg:               1.296
smc73-m02:     Duration Min:               0.446
smc73-m02:     Ttfb Max:                   1.949
smc73-m02:     Ttfb Avg:                   1.296
smc73-m02:     Ttfb Min:                   0.446
smc73-m02:     Duration 90th-ile:          1.540
smc73-m02:     Duration 99th-ile:          1.687
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         374.039
smc73-m02:     Total Transferred (MB):     2304.000
smc73-m02:     Ttfb 90th-ile:              1.540
smc73-m02:     Ttfb 99th-ile:              1.687
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       138240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    132.510
smc73-m02:     Duration Max:               0.901
smc73-m02:     Duration Avg:               0.060
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   0.873
smc73-m02:     Ttfb Avg:                   0.035
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.096
smc73-m02:     Duration 99th-ile:          0.147
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         260.810
smc73-m02:     Total Transferred (MB):     34560.000
smc73-m02:     Ttfb 90th-ile:              0.067
smc73-m02:     Ttfb 99th-ile:              0.113
```


# 4. 16MB throughput, 128-512 sessions, 1 minute test

## 4.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 6
  batch_id: 16m-throughput-v01
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 5120 -c 128 -o 16Mb -e 3 -- -sampleReads 6
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 5120 -c 256 -o 16Mb -e 3 -- -sampleReads 6
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 5376 -c 384 -o 16Mb -e 3 -- -sampleReads 6
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 5120 -c 512 -o 16Mb -e 3 -- -sampleReads 6

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 4.2. 128 sessions

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                6
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1370.848
smc73-m02:     Duration Max:               5.759
smc73-m02:     Duration Avg:               1.468
smc73-m02:     Duration Min:               0.592
smc73-m02:     Ttfb Max:                   5.759
smc73-m02:     Ttfb Avg:                   1.468
smc73-m02:     Ttfb Min:                   0.592
smc73-m02:     Duration 90th-ile:          3.748
smc73-m02:     Duration 99th-ile:          4.960
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         59.759
smc73-m02:     Total Transferred (MB):     81920.000
smc73-m02:     Ttfb 90th-ile:              3.748
smc73-m02:     Ttfb 99th-ile:              4.960
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       30720
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6822.588
smc73-m02:     Duration Max:               1.320
smc73-m02:     Duration Avg:               0.300
smc73-m02:     Duration Min:               0.051
smc73-m02:     Ttfb Max:                   1.011
smc73-m02:     Ttfb Avg:                   0.170
smc73-m02:     Ttfb Min:                   0.041
smc73-m02:     Duration 90th-ile:          0.468
smc73-m02:     Duration 99th-ile:          0.684
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         72.043
smc73-m02:     Total Transferred (MB):     491520.000
smc73-m02:     Ttfb 90th-ile:              0.238
smc73-m02:     Ttfb 99th-ile:              0.529
```

## 4.3. 256 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                6
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1335.865
smc73-m02:     Duration Max:               12.596
smc73-m02:     Duration Avg:               2.946
smc73-m02:     Duration Min:               0.598
smc73-m02:     Ttfb Max:                   12.596
smc73-m02:     Ttfb Avg:                   2.946
smc73-m02:     Ttfb Min:                   0.598
smc73-m02:     Duration 90th-ile:          5.562
smc73-m02:     Duration 99th-ile:          8.936
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         61.324
smc73-m02:     Total Transferred (MB):     81920.000
smc73-m02:     Ttfb 90th-ile:              5.562
smc73-m02:     Ttfb 99th-ile:              8.936
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       30720
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    8670.475
smc73-m02:     Duration Max:               2.413
smc73-m02:     Duration Avg:               0.461
smc73-m02:     Duration Min:               0.111
smc73-m02:     Ttfb Max:                   2.176
smc73-m02:     Ttfb Avg:                   0.384
smc73-m02:     Ttfb Min:                   0.073
smc73-m02:     Duration 90th-ile:          0.640
smc73-m02:     Duration 99th-ile:          1.184
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         56.689
smc73-m02:     Total Transferred (MB):     491520.000
smc73-m02:     Ttfb 90th-ile:              0.494
smc73-m02:     Ttfb 99th-ile:              1.024
```

## 4.4. 384 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 5376
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                6
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5376
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1687.900
smc73-m02:     Duration Max:               16.001
smc73-m02:     Duration Avg:               3.467
smc73-m02:     Duration Min:               0.678
smc73-m02:     Ttfb Max:                   16.001
smc73-m02:     Ttfb Avg:                   3.467
smc73-m02:     Ttfb Min:                   0.678
smc73-m02:     Duration 90th-ile:          7.350
smc73-m02:     Duration 99th-ile:          10.511
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         50.960
smc73-m02:     Total Transferred (MB):     86016.000
smc73-m02:     Ttfb 90th-ile:              7.350
smc73-m02:     Ttfb 99th-ile:              10.511
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       32256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    8029.551
smc73-m02:     Duration Max:               4.510
smc73-m02:     Duration Avg:               0.760
smc73-m02:     Duration Min:               0.082
smc73-m02:     Ttfb Max:                   4.323
smc73-m02:     Ttfb Avg:                   0.675
smc73-m02:     Ttfb Min:                   0.062
smc73-m02:     Duration 90th-ile:          0.916
smc73-m02:     Duration 99th-ile:          1.485
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         64.275
smc73-m02:     Total Transferred (MB):     516096.000
smc73-m02:     Ttfb 90th-ile:              0.816
smc73-m02:     Ttfb 99th-ile:              1.255
```

## 4.5. 512 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                6
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1617.107
smc73-m02:     Duration Max:               17.587
smc73-m02:     Duration Avg:               4.782
smc73-m02:     Duration Min:               0.732
smc73-m02:     Ttfb Max:                   17.587
smc73-m02:     Ttfb Avg:                   4.782
smc73-m02:     Ttfb Min:                   0.732
smc73-m02:     Duration 90th-ile:          9.107
smc73-m02:     Duration 99th-ile:          13.236
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         50.658
smc73-m02:     Total Transferred (MB):     81920.000
smc73-m02:     Ttfb 90th-ile:              9.107
smc73-m02:     Ttfb 99th-ile:              13.236
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       30720
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    9275.543
smc73-m02:     Duration Max:               2.324
smc73-m02:     Duration Avg:               0.873
smc73-m02:     Duration Min:               0.194
smc73-m02:     Ttfb Max:                   1.687
smc73-m02:     Ttfb Avg:                   0.817
smc73-m02:     Ttfb Min:                   0.179
smc73-m02:     Duration 90th-ile:          1.028
smc73-m02:     Duration 99th-ile:          1.396
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         52.991
smc73-m02:     Total Transferred (MB):     491520.000
smc73-m02:     Ttfb 90th-ile:              0.957
smc73-m02:     Ttfb 99th-ile:              1.157
```


# 5. 16MB throughput, 128-512 sessions, 2 minutes test

## 5.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 6
  batch_id: 16m-throughput-v02 - double obj cnt
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 128 -o 16Mb -e 3 -- -sampleReads 6
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 256 -o 16Mb -e 3 -- -sampleReads 6
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10752 -c 384 -o 16Mb -e 3 -- -sampleReads 6
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 512 -o 16Mb -e 3 -- -sampleReads 6

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 5.2. 128 sessions

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                6
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1482.389
smc73-m02:     Duration Max:               8.458
smc73-m02:     Duration Avg:               1.370
smc73-m02:     Duration Min:               0.610
smc73-m02:     Ttfb Max:                   8.458
smc73-m02:     Ttfb Avg:                   1.370
smc73-m02:     Ttfb Min:                   0.610
smc73-m02:     Duration 90th-ile:          1.990
smc73-m02:     Duration 99th-ile:          4.950
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         110.524
smc73-m02:     Total Transferred (MB):     163840.000
smc73-m02:     Ttfb 90th-ile:              1.990
smc73-m02:     Ttfb 99th-ile:              4.950
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       61440
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6759.491
smc73-m02:     Duration Max:               3.734
smc73-m02:     Duration Avg:               0.303
smc73-m02:     Duration Min:               0.049
smc73-m02:     Ttfb Max:                   3.568
smc73-m02:     Ttfb Avg:                   0.173
smc73-m02:     Ttfb Min:                   0.039
smc73-m02:     Duration 90th-ile:          0.456
smc73-m02:     Duration 99th-ile:          0.720
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         145.431
smc73-m02:     Total Transferred (MB):     983040.000
smc73-m02:     Ttfb 90th-ile:              0.254
smc73-m02:     Ttfb 99th-ile:              0.527
workload 3
```

## 5.3. 256 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                6
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1352.390
smc73-m02:     Duration Max:               12.867
smc73-m02:     Duration Avg:               2.985
smc73-m02:     Duration Min:               0.614
smc73-m02:     Ttfb Max:                   12.867
smc73-m02:     Ttfb Avg:                   2.985
smc73-m02:     Ttfb Min:                   0.614
smc73-m02:     Duration 90th-ile:          5.771
smc73-m02:     Duration 99th-ile:          8.946
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         121.148
smc73-m02:     Total Transferred (MB):     163840.000
smc73-m02:     Ttfb 90th-ile:              5.771
smc73-m02:     Ttfb 99th-ile:              8.946
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       61440
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    8440.254
smc73-m02:     Duration Max:               1.719
smc73-m02:     Duration Avg:               0.483
smc73-m02:     Duration Min:               0.100
smc73-m02:     Ttfb Max:                   1.473
smc73-m02:     Ttfb Avg:                   0.363
smc73-m02:     Ttfb Min:                   0.070
smc73-m02:     Duration 90th-ile:          0.740
smc73-m02:     Duration 99th-ile:          1.056
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         116.470
smc73-m02:     Total Transferred (MB):     983040.000
smc73-m02:     Ttfb 90th-ile:              0.498
smc73-m02:     Ttfb 99th-ile:              0.852
```

## 5.4. 384 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 10752
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                6
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10752
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1502.122
smc73-m02:     Duration Max:               16.724
smc73-m02:     Duration Avg:               4.026
smc73-m02:     Duration Min:               0.635
smc73-m02:     Ttfb Max:                   16.724
smc73-m02:     Ttfb Avg:                   4.026
smc73-m02:     Ttfb Min:                   0.635
smc73-m02:     Duration 90th-ile:          7.975
smc73-m02:     Duration 99th-ile:          10.298
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         114.526
smc73-m02:     Total Transferred (MB):     172032.000
smc73-m02:     Ttfb 90th-ile:              7.975
smc73-m02:     Ttfb 99th-ile:              10.298
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       64512
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    8822.406
smc73-m02:     Duration Max:               2.047
smc73-m02:     Duration Avg:               0.694
smc73-m02:     Duration Min:               0.163
smc73-m02:     Ttfb Max:                   1.656
smc73-m02:     Ttfb Avg:                   0.625
smc73-m02:     Ttfb Min:                   0.144
smc73-m02:     Duration 90th-ile:          0.916
smc73-m02:     Duration 99th-ile:          1.269
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         116.997
smc73-m02:     Total Transferred (MB):     1032192.000
smc73-m02:     Ttfb 90th-ile:              0.813
smc73-m02:     Ttfb 99th-ile:              1.148
```

## 5.5. 512 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                6
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1592.573
smc73-m02:     Duration Max:               18.586
smc73-m02:     Duration Avg:               5.045
smc73-m02:     Duration Min:               0.709
smc73-m02:     Ttfb Max:                   18.586
smc73-m02:     Ttfb Avg:                   5.045
smc73-m02:     Ttfb Min:                   0.709
smc73-m02:     Duration 90th-ile:          9.456
smc73-m02:     Duration 99th-ile:          13.926
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         102.878
smc73-m02:     Total Transferred (MB):     163840.000
smc73-m02:     Ttfb 90th-ile:              9.456
smc73-m02:     Ttfb 99th-ile:              13.926
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       61440
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    8975.843
smc73-m02:     Duration Max:               2.803
smc73-m02:     Duration Avg:               0.904
smc73-m02:     Duration Min:               0.147
smc73-m02:     Ttfb Max:                   2.622
smc73-m02:     Ttfb Avg:                   0.839
smc73-m02:     Ttfb Min:                   0.135
smc73-m02:     Duration 90th-ile:          1.124
smc73-m02:     Duration 99th-ile:          1.548
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         109.521
smc73-m02:     Total Transferred (MB):     983040.000
smc73-m02:     Ttfb 90th-ile:              1.031
smc73-m02:     Ttfb 99th-ile:              1.379
```


# 6. 16MB throughput, 32-100 sessions, 2 minutes test

## 6.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 6
  batch_id: 16m-throughput-v03
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 2560 -c  32 -o 16Mb -e 3 -- -sampleReads 5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 4480 -c  64 -o 16Mb -e 3 -- -sampleReads 8
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 5600 -c  80 -o 16Mb -e 3 -- -sampleReads 9
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 7000 -c 100 -o 16Mb -e 3 -- -sampleReads 7

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 6.2. 32 sessions

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    356.060
smc73-m02:     Duration Max:               2.828
smc73-m02:     Duration Avg:               1.426
smc73-m02:     Duration Min:               0.783
smc73-m02:     Ttfb Max:                   2.828
smc73-m02:     Ttfb Avg:                   1.426
smc73-m02:     Ttfb Min:                   0.783
smc73-m02:     Duration 90th-ile:          1.703
smc73-m02:     Duration 99th-ile:          2.085
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         115.037
smc73-m02:     Total Transferred (MB):     40960.000
smc73-m02:     Ttfb 90th-ile:              1.703
smc73-m02:     Ttfb 99th-ile:              2.085
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       12800
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    4047.924
smc73-m02:     Duration Max:               2.435
smc73-m02:     Duration Avg:               0.126
smc73-m02:     Duration Min:               0.045
smc73-m02:     Ttfb Max:                   2.408
smc73-m02:     Ttfb Avg:                   0.102
smc73-m02:     Ttfb Min:                   0.036
smc73-m02:     Duration 90th-ile:          0.170
smc73-m02:     Duration 99th-ile:          0.351
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         50.594
smc73-m02:     Total Transferred (MB):     204800.000
smc73-m02:     Ttfb 90th-ile:              0.142
smc73-m02:     Ttfb 99th-ile:              0.309
```

## 6.3. 64 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 4480
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                8
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       4480
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    758.092
smc73-m02:     Duration Max:               4.078
smc73-m02:     Duration Avg:               1.336
smc73-m02:     Duration Min:               0.719
smc73-m02:     Ttfb Max:                   4.078
smc73-m02:     Ttfb Avg:                   1.336
smc73-m02:     Ttfb Min:                   0.719
smc73-m02:     Duration 90th-ile:          1.590
smc73-m02:     Duration 99th-ile:          3.456
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         94.553
smc73-m02:     Total Transferred (MB):     71680.000
smc73-m02:     Ttfb 90th-ile:              1.590
smc73-m02:     Ttfb 99th-ile:              3.456
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       35840
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5503.244
smc73-m02:     Duration Max:               4.376
smc73-m02:     Duration Avg:               0.186
smc73-m02:     Duration Min:               0.047
smc73-m02:     Ttfb Max:                   4.288
smc73-m02:     Ttfb Avg:                   0.150
smc73-m02:     Ttfb Min:                   0.037
smc73-m02:     Duration 90th-ile:          0.243
smc73-m02:     Duration 99th-ile:          0.579
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         104.200
smc73-m02:     Total Transferred (MB):     573440.000
smc73-m02:     Ttfb 90th-ile:              0.197
smc73-m02:     Ttfb 99th-ile:              0.522
```

## 6.4. 80 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 80
smc73-m02:     numSamples:                 5600
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                9
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1097.432
smc73-m02:     Duration Max:               3.888
smc73-m02:     Duration Avg:               1.153
smc73-m02:     Duration Min:               0.600
smc73-m02:     Ttfb Max:                   3.888
smc73-m02:     Ttfb Avg:                   1.153
smc73-m02:     Ttfb Min:                   0.600
smc73-m02:     Duration 90th-ile:          1.418
smc73-m02:     Duration 99th-ile:          2.238
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         81.645
smc73-m02:     Total Transferred (MB):     89600.000
smc73-m02:     Ttfb 90th-ile:              1.418
smc73-m02:     Ttfb 99th-ile:              2.238
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       50400
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5995.145
smc73-m02:     Duration Max:               4.144
smc73-m02:     Duration Avg:               0.212
smc73-m02:     Duration Min:               0.048
smc73-m02:     Ttfb Max:                   4.112
smc73-m02:     Ttfb Avg:                   0.144
smc73-m02:     Ttfb Min:                   0.037
smc73-m02:     Duration 90th-ile:          0.303
smc73-m02:     Duration 99th-ile:          0.573
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         134.509
smc73-m02:     Total Transferred (MB):     806400.000
smc73-m02:     Ttfb 90th-ile:              0.204
smc73-m02:     Ttfb 99th-ile:              0.477
```

## 6.5. 100 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 100
smc73-m02:     numSamples:                 7000
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                7
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       7000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1349.856
smc73-m02:     Duration Max:               5.705
smc73-m02:     Duration Avg:               1.168
smc73-m02:     Duration Min:               0.590
smc73-m02:     Ttfb Max:                   5.705
smc73-m02:     Ttfb Avg:                   1.168
smc73-m02:     Ttfb Min:                   0.590
smc73-m02:     Duration 90th-ile:          1.475
smc73-m02:     Duration 99th-ile:          5.091
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         82.972
smc73-m02:     Total Transferred (MB):     112000.000
smc73-m02:     Ttfb 90th-ile:              1.475
smc73-m02:     Ttfb 99th-ile:              5.091
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       49000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6485.781
smc73-m02:     Duration Max:               4.191
smc73-m02:     Duration Avg:               0.246
smc73-m02:     Duration Min:               0.049
smc73-m02:     Ttfb Max:                   4.158
smc73-m02:     Ttfb Avg:                   0.169
smc73-m02:     Ttfb Min:                   0.041
smc73-m02:     Duration 90th-ile:          0.355
smc73-m02:     Duration 99th-ile:          0.597
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         120.880
smc73-m02:     Total Transferred (MB):     784000.000
smc73-m02:     Ttfb 90th-ile:              0.239
smc73-m02:     Ttfb 99th-ile:              0.478
```


# 7. TTFB, 100b, 1-128 sessions - too short, ignore

## 7.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 7
  batch_id: ttfb - quick test nr.1
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 256 -c 1 -o 100b -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 2560 -c 16 -o 100b -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 2560 -c 32 -o 100b -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 2560 -c 64 -o 100b -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 2560 -c 128 -o 100b -e 3

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 7.2. 1 session -- to be ignored, too quick read phase (4sec)

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 256
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                1
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.000
smc73-m02:     Duration Max:               2.250
smc73-m02:     Duration Avg:               1.556
smc73-m02:     Duration Min:               1.520
smc73-m02:     Ttfb Max:                   2.250
smc73-m02:     Ttfb Avg:                   1.556
smc73-m02:     Ttfb Min:                   1.520
smc73-m02:     Duration 90th-ile:          1.577
smc73-m02:     Duration 99th-ile:          2.136
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         398.455
smc73-m02:     Total Transferred (MB):     0.024
smc73-m02:     Ttfb 90th-ile:              1.577
smc73-m02:     Ttfb 99th-ile:              2.136
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.007
smc73-m02:     Duration Max:               0.032
smc73-m02:     Duration Avg:               0.014
smc73-m02:     Duration Min:               0.011
smc73-m02:     Ttfb Max:                   0.032
smc73-m02:     Ttfb Avg:                   0.014
smc73-m02:     Ttfb Min:                   0.011
smc73-m02:     Duration 90th-ile:          0.016
smc73-m02:     Duration 99th-ile:          0.029
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         3.538
smc73-m02:     Total Transferred (MB):     0.024
smc73-m02:     Ttfb 90th-ile:              0.016
smc73-m02:     Ttfb 99th-ile:              0.029
```


# 8. TTFB, 100 bytes, 1-512 sessions - take 2

## 8.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 5
  batch_id: ttfb-v01
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   256 -c   1 -o 100b -e 3 -- -sampleReads 40
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  16 -o 100b -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  32 -o 100b -e 3 -- -sampleReads 20
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c  64 -o 100b -e 3 -- -sampleReads 25
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 128 -o 100b -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 256 -o 100b -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10368 -c 384 -o 100b -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 512 -o 100b -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 8.2. 1 session

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 256
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                40
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.000
smc73-m02:     Duration Max:               2.259
smc73-m02:     Duration Avg:               1.554
smc73-m02:     Duration Min:               1.520
smc73-m02:     Ttfb Max:                   2.259
smc73-m02:     Ttfb Avg:                   1.554
smc73-m02:     Ttfb Min:                   1.520
smc73-m02:     Duration 90th-ile:          1.564
smc73-m02:     Duration 99th-ile:          2.134
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         397.942
smc73-m02:     Total Transferred (MB):     0.024
smc73-m02:     Ttfb 90th-ile:              1.564
smc73-m02:     Ttfb 99th-ile:              2.134
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.007
smc73-m02:     Duration Max:               0.171
smc73-m02:     Duration Avg:               0.014
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   0.171
smc73-m02:     Ttfb Avg:                   0.014
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.016
smc73-m02:     Duration 99th-ile:          0.027
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         140.683
smc73-m02:     Total Transferred (MB):     0.977
smc73-m02:     Ttfb 90th-ile:              0.016
smc73-m02:     Ttfb 99th-ile:              0.027
```

## 8.3. 16 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.001
smc73-m02:     Duration Max:               2.131
smc73-m02:     Duration Avg:               1.443
smc73-m02:     Duration Min:               0.648
smc73-m02:     Ttfb Max:                   2.131
smc73-m02:     Ttfb Avg:                   1.443
smc73-m02:     Ttfb Min:                   0.648
smc73-m02:     Duration 90th-ile:          1.527
smc73-m02:     Duration 99th-ile:          1.648
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         231.866
smc73-m02:     Total Transferred (MB):     0.244
smc73-m02:     Ttfb 90th-ile:              1.527
smc73-m02:     Ttfb 99th-ile:              1.648
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       38400
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.043
smc73-m02:     Duration Max:               1.250
smc73-m02:     Duration Avg:               0.036
smc73-m02:     Duration Min:               0.009
smc73-m02:     Ttfb Max:                   1.250
smc73-m02:     Ttfb Avg:                   0.036
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.074
smc73-m02:     Duration 99th-ile:          0.162
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         85.411
smc73-m02:     Total Transferred (MB):     3.662
smc73-m02:     Ttfb 90th-ile:              0.074
smc73-m02:     Ttfb 99th-ile:              0.162
```

## 8.4. 32 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                20
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.002
smc73-m02:     Duration Max:               1.878
smc73-m02:     Duration Avg:               1.438
smc73-m02:     Duration Min:               0.671
smc73-m02:     Ttfb Max:                   1.878
smc73-m02:     Ttfb Avg:                   1.438
smc73-m02:     Ttfb Min:                   0.671
smc73-m02:     Duration 90th-ile:          1.536
smc73-m02:     Duration 99th-ile:          1.595
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         115.724
smc73-m02:     Total Transferred (MB):     0.244
smc73-m02:     Ttfb 90th-ile:              1.536
smc73-m02:     Ttfb 99th-ile:              1.595
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.075
smc73-m02:     Duration Max:               0.582
smc73-m02:     Duration Avg:               0.041
smc73-m02:     Duration Min:               0.008
smc73-m02:     Ttfb Max:                   0.582
smc73-m02:     Ttfb Avg:                   0.041
smc73-m02:     Ttfb Min:                   0.008
smc73-m02:     Duration 90th-ile:          0.076
smc73-m02:     Duration 99th-ile:          0.140
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         65.253
smc73-m02:     Total Transferred (MB):     4.883
smc73-m02:     Ttfb 90th-ile:              0.076
smc73-m02:     Ttfb 99th-ile:              0.140
```

## 8.5. 64 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                25
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.005
smc73-m02:     Duration Max:               2.016
smc73-m02:     Duration Avg:               1.337
smc73-m02:     Duration Min:               0.604
smc73-m02:     Ttfb Max:                   2.016
smc73-m02:     Ttfb Avg:                   1.337
smc73-m02:     Ttfb Min:                   0.604
smc73-m02:     Duration 90th-ile:          1.558
smc73-m02:     Duration 99th-ile:          1.606
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         107.755
smc73-m02:     Total Transferred (MB):     0.488
smc73-m02:     Ttfb 90th-ile:              1.558
smc73-m02:     Ttfb 99th-ile:              1.606
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       128000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.115
smc73-m02:     Duration Max:               1.395
smc73-m02:     Duration Avg:               0.053
smc73-m02:     Duration Min:               0.009
smc73-m02:     Ttfb Max:                   1.395
smc73-m02:     Ttfb Avg:                   0.053
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.081
smc73-m02:     Duration 99th-ile:          0.124
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         105.980
smc73-m02:     Total Transferred (MB):     12.207
smc73-m02:     Ttfb 90th-ile:              0.081
smc73-m02:     Ttfb 99th-ile:              0.124
```

## 8.6. 128 sessions

```
workload 10
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.008
smc73-m02:     Duration Max:               2.996
smc73-m02:     Duration Avg:               1.438
smc73-m02:     Duration Min:               0.663
smc73-m02:     Ttfb Max:                   2.996
smc73-m02:     Ttfb Avg:                   1.438
smc73-m02:     Ttfb Min:                   0.663
smc73-m02:     Duration 90th-ile:          1.698
smc73-m02:     Duration 99th-ile:          2.509
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         115.988
smc73-m02:     Total Transferred (MB):     0.977
smc73-m02:     Ttfb 90th-ile:              1.698
smc73-m02:     Ttfb 99th-ile:              2.509
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.138
smc73-m02:     Duration Max:               1.431
smc73-m02:     Duration Avg:               0.089
smc73-m02:     Duration Min:               0.009
smc73-m02:     Ttfb Max:                   1.431
smc73-m02:     Ttfb Avg:                   0.089
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.122
smc73-m02:     Duration 99th-ile:          0.179
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         106.268
smc73-m02:     Total Transferred (MB):     14.648
smc73-m02:     Ttfb 90th-ile:              0.122
smc73-m02:     Ttfb 99th-ile:              0.179
```

## 8.7. 256 sessions

```
workload 12
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.020
smc73-m02:     Duration Max:               4.594
smc73-m02:     Duration Avg:               1.210
smc73-m02:     Duration Min:               0.293
smc73-m02:     Ttfb Max:                   4.594
smc73-m02:     Ttfb Avg:                   1.210
smc73-m02:     Ttfb Min:                   0.293
smc73-m02:     Duration 90th-ile:          2.656
smc73-m02:     Duration 99th-ile:          3.724
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         49.220
smc73-m02:     Total Transferred (MB):     0.977
smc73-m02:     Ttfb 90th-ile:              2.656
smc73-m02:     Ttfb 99th-ile:              3.724
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.144
smc73-m02:     Duration Max:               1.579
smc73-m02:     Duration Avg:               0.169
smc73-m02:     Duration Min:               0.026
smc73-m02:     Ttfb Max:                   1.579
smc73-m02:     Ttfb Avg:                   0.169
smc73-m02:     Ttfb Min:                   0.026
smc73-m02:     Duration 90th-ile:          0.207
smc73-m02:     Duration 99th-ile:          0.403
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         101.771
smc73-m02:     Total Transferred (MB):     14.648
smc73-m02:     Ttfb 90th-ile:              0.207
smc73-m02:     Ttfb 99th-ile:              0.403
```

## 8.8. 384 sessions

```
workload 14
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 10368
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10368
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.021
smc73-m02:     Duration Max:               8.466
smc73-m02:     Duration Avg:               1.712
smc73-m02:     Duration Min:               0.428
smc73-m02:     Ttfb Max:                   8.466
smc73-m02:     Ttfb Avg:                   1.712
smc73-m02:     Ttfb Min:                   0.428
smc73-m02:     Duration 90th-ile:          3.847
smc73-m02:     Duration 99th-ile:          5.476
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         47.435
smc73-m02:     Total Transferred (MB):     0.989
smc73-m02:     Ttfb 90th-ile:              3.847
smc73-m02:     Ttfb 99th-ile:              5.476
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       155520
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.102
smc73-m02:     Duration Max:               1.777
smc73-m02:     Duration Avg:               0.360
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   1.777
smc73-m02:     Ttfb Avg:                   0.360
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.405
smc73-m02:     Duration 99th-ile:          0.587
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         145.982
smc73-m02:     Total Transferred (MB):     14.832
smc73-m02:     Ttfb 90th-ile:              0.405
smc73-m02:     Ttfb 99th-ile:              0.587
```

## 8.9. 512 sessions

```
workload 16
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.023
smc73-m02:     Duration Max:               14.546
smc73-m02:     Duration Avg:               2.101
smc73-m02:     Duration Min:               0.407
smc73-m02:     Ttfb Max:                   14.546
smc73-m02:     Ttfb Avg:                   2.101
smc73-m02:     Ttfb Min:                   0.407
smc73-m02:     Duration 90th-ile:          4.444
smc73-m02:     Duration 99th-ile:          12.278
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         43.065
smc73-m02:     Total Transferred (MB):     0.977
smc73-m02:     Ttfb 90th-ile:              4.444
smc73-m02:     Ttfb 99th-ile:              12.278
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.066
smc73-m02:     Duration Max:               2.725
smc73-m02:     Duration Avg:               0.743
smc73-m02:     Duration Min:               0.017
smc73-m02:     Ttfb Max:                   2.725
smc73-m02:     Ttfb Avg:                   0.743
smc73-m02:     Ttfb Min:                   0.017
smc73-m02:     Duration 90th-ile:          0.830
smc73-m02:     Duration 99th-ile:          1.163
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         223.169
smc73-m02:     Total Transferred (MB):     14.648
smc73-m02:     Ttfb 90th-ile:              0.830
smc73-m02:     Ttfb 99th-ile:              1.163
```


# 9. TTFB, 100 bytes, 900 sessions - FAILED

## 9.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 5
  batch_id: ttfb-v02.900
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 900 -o 100b -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 9.2. 900 sessions

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 900
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10222
smc73-m02:     Errors Count:               18
smc73-m02:     Total Throughput (MB/s):    0.026
smc73-m02:     Duration Max:               24.366
smc73-m02:     Duration Avg:               3.095
smc73-m02:     Duration Min:               0.352
smc73-m02:     Ttfb Max:                   24.366
smc73-m02:     Ttfb Avg:                   3.095
smc73-m02:     Ttfb Min:                   0.352
smc73-m02:     Duration 90th-ile:          10.122
smc73-m02:     Duration 99th-ile:          14.859
smc73-m02:     Errors:
smc73-m02:        Write(5377) completed in 23.42s with error ServiceUnavailable: Reduce your request rate
smc73-m02:      status code: 503, request id: , host id:
....repeats 18 times....
smc73-m02:     Total Duration (s):         38.227
smc73-m02:     Total Transferred (MB):     0.975
smc73-m02:     Ttfb 90th-ile:              10.122
smc73-m02:     Ttfb 99th-ile:              14.859
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       152975
smc73-m02:     Errors Count:               625
smc73-m02:     Total Throughput (MB/s):    0.068
smc73-m02:     Duration Max:               17.780
smc73-m02:     Duration Avg:               1.214
smc73-m02:     Duration Min:               0.026
smc73-m02:     Ttfb Max:                   17.780
smc73-m02:     Ttfb Avg:                   1.214
smc73-m02:     Ttfb Min:                   0.017
smc73-m02:     Duration 90th-ile:          1.500
smc73-m02:     Duration 99th-ile:          1.766
smc73-m02:     Errors:
smc73-m02:        Read(42) completed in 0.10s with error expected object length 100, actual 0
..... repeats 18 * 15 times .....
smc73-m02:     Total Duration (s):         214.018
smc73-m02:     Total Transferred (MB):     14.589
smc73-m02:     Ttfb 90th-ile:              1.500
smc73-m02:     Ttfb 99th-ile:              1.766
```




# 10. TTFB, 1 KB, 1-512 sessions

## 10.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 1
  batch_id: ttfb-v03-1Kb
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   256 -c   1 -o 1Kb -e 3 -- -sampleReads 40
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  16 -o 1Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  32 -o 1Kb -e 3 -- -sampleReads 20
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c  64 -o 1Kb -e 3 -- -sampleReads 25
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 128 -o 1Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 256 -o 1Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10368 -c 384 -o 1Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 512 -o 1Kb -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 10.2. 1 session

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 256
smc73-m02:     objectSize (MB):            0.001
smc73-m02:     sampleReads:                40
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.001
smc73-m02:     Duration Max:               2.220
smc73-m02:     Duration Avg:               1.559
smc73-m02:     Duration Min:               1.521
smc73-m02:     Ttfb Max:                   2.220
smc73-m02:     Ttfb Avg:                   1.559
smc73-m02:     Ttfb Min:                   1.521
smc73-m02:     Duration 90th-ile:          1.572
smc73-m02:     Duration 99th-ile:          2.172
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         399.057
smc73-m02:     Total Transferred (MB):     0.250
smc73-m02:     Ttfb 90th-ile:              1.572
smc73-m02:     Ttfb 99th-ile:              2.172
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.071
smc73-m02:     Duration Max:               0.091
smc73-m02:     Duration Avg:               0.014
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   0.091
smc73-m02:     Ttfb Avg:                   0.014
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.016
smc73-m02:     Duration 99th-ile:          0.026
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         140.914
smc73-m02:     Total Transferred (MB):     10.000
smc73-m02:     Ttfb 90th-ile:              0.016
smc73-m02:     Ttfb 99th-ile:              0.026
```

## 10.3. 16 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.001
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.011
smc73-m02:     Duration Max:               1.863
smc73-m02:     Duration Avg:               1.453
smc73-m02:     Duration Min:               0.695
smc73-m02:     Ttfb Max:                   1.863
smc73-m02:     Ttfb Avg:                   1.453
smc73-m02:     Ttfb Min:                   0.695
smc73-m02:     Duration 90th-ile:          1.528
smc73-m02:     Duration 99th-ile:          1.668
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         233.440
smc73-m02:     Total Transferred (MB):     2.500
smc73-m02:     Ttfb 90th-ile:              1.528
smc73-m02:     Ttfb 99th-ile:              1.668
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       38400
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.414
smc73-m02:     Duration Max:               0.902
smc73-m02:     Duration Avg:               0.038
smc73-m02:     Duration Min:               0.009
smc73-m02:     Ttfb Max:                   0.902
smc73-m02:     Ttfb Avg:                   0.038
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.080
smc73-m02:     Duration 99th-ile:          0.218
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         90.556
smc73-m02:     Total Transferred (MB):     37.500
smc73-m02:     Ttfb 90th-ile:              0.080
smc73-m02:     Ttfb 99th-ile:              0.218
```

## 10.4. 32 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.001
smc73-m02:     sampleReads:                20
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.025
smc73-m02:     Duration Max:               1.897
smc73-m02:     Duration Avg:               1.265
smc73-m02:     Duration Min:               0.621
smc73-m02:     Ttfb Max:                   1.897
smc73-m02:     Ttfb Avg:                   1.265
smc73-m02:     Ttfb Min:                   0.621
smc73-m02:     Duration 90th-ile:          1.533
smc73-m02:     Duration 99th-ile:          1.623
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         101.956
smc73-m02:     Total Transferred (MB):     2.500
smc73-m02:     Ttfb 90th-ile:              1.533
smc73-m02:     Ttfb 99th-ile:              1.623
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.732
smc73-m02:     Duration Max:               0.792
smc73-m02:     Duration Avg:               0.042
smc73-m02:     Duration Min:               0.009
smc73-m02:     Ttfb Max:                   0.792
smc73-m02:     Ttfb Avg:                   0.042
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.080
smc73-m02:     Duration 99th-ile:          0.137
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         68.261
smc73-m02:     Total Transferred (MB):     50.000
smc73-m02:     Ttfb 90th-ile:              0.080
smc73-m02:     Ttfb 99th-ile:              0.137
```

## 10.5. 64 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            0.001
smc73-m02:     sampleReads:                25
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.048
smc73-m02:     Duration Max:               1.979
smc73-m02:     Duration Avg:               1.285
smc73-m02:     Duration Min:               0.602
smc73-m02:     Ttfb Max:                   1.979
smc73-m02:     Ttfb Avg:                   1.285
smc73-m02:     Ttfb Min:                   0.602
smc73-m02:     Duration 90th-ile:          1.551
smc73-m02:     Duration 99th-ile:          1.654
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         103.571
smc73-m02:     Total Transferred (MB):     5.000
smc73-m02:     Ttfb 90th-ile:              1.551
smc73-m02:     Ttfb 99th-ile:              1.654
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       128000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1.139
smc73-m02:     Duration Max:               1.288
smc73-m02:     Duration Avg:               0.055
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   1.288
smc73-m02:     Ttfb Avg:                   0.055
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.084
smc73-m02:     Duration 99th-ile:          0.128
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         109.775
smc73-m02:     Total Transferred (MB):     125.000
smc73-m02:     Ttfb 90th-ile:              0.084
smc73-m02:     Ttfb 99th-ile:              0.128
```

## 10.6. 128 sessions

```
workload 10
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.001
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.086
smc73-m02:     Duration Max:               2.839
smc73-m02:     Duration Avg:               1.435
smc73-m02:     Duration Min:               0.539
smc73-m02:     Ttfb Max:                   2.839
smc73-m02:     Ttfb Avg:                   1.435
smc73-m02:     Ttfb Min:                   0.539
smc73-m02:     Duration 90th-ile:          1.641
smc73-m02:     Duration 99th-ile:          2.225
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         115.703
smc73-m02:     Total Transferred (MB):     10.000
smc73-m02:     Ttfb 90th-ile:              1.641
smc73-m02:     Ttfb 99th-ile:              2.225
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1.388
smc73-m02:     Duration Max:               1.264
smc73-m02:     Duration Avg:               0.090
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   1.264
smc73-m02:     Ttfb Avg:                   0.090
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.127
smc73-m02:     Duration 99th-ile:          0.196
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         108.088
smc73-m02:     Total Transferred (MB):     150.000
smc73-m02:     Ttfb 90th-ile:              0.127
smc73-m02:     Ttfb 99th-ile:              0.196
```

## 10.7. 256 sessions

```
workload 12
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.001
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.211
smc73-m02:     Duration Max:               4.277
smc73-m02:     Duration Avg:               1.165
smc73-m02:     Duration Min:               0.341
smc73-m02:     Ttfb Max:                   4.277
smc73-m02:     Ttfb Avg:                   1.165
smc73-m02:     Ttfb Min:                   0.341
smc73-m02:     Duration 90th-ile:          2.279
smc73-m02:     Duration 99th-ile:          3.205
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         47.456
smc73-m02:     Total Transferred (MB):     10.000
smc73-m02:     Ttfb 90th-ile:              2.279
smc73-m02:     Ttfb 99th-ile:              3.205
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1.128
smc73-m02:     Duration Max:               1.237
smc73-m02:     Duration Avg:               0.221
smc73-m02:     Duration Min:               0.015
smc73-m02:     Ttfb Max:                   1.237
smc73-m02:     Ttfb Avg:                   0.221
smc73-m02:     Ttfb Min:                   0.015
smc73-m02:     Duration 90th-ile:          0.269
smc73-m02:     Duration 99th-ile:          0.405
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         132.951
smc73-m02:     Total Transferred (MB):     150.000
smc73-m02:     Ttfb 90th-ile:              0.269
smc73-m02:     Ttfb 99th-ile:              0.405
```

## 10.8. 384 sessions

```
workload 14
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 10368
smc73-m02:     objectSize (MB):            0.001
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10368
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.245
smc73-m02:     Duration Max:               8.167
smc73-m02:     Duration Avg:               1.493
smc73-m02:     Duration Min:               0.411
smc73-m02:     Ttfb Max:                   8.167
smc73-m02:     Ttfb Avg:                   1.493
smc73-m02:     Ttfb Min:                   0.411
smc73-m02:     Duration 90th-ile:          2.842
smc73-m02:     Duration 99th-ile:          4.729
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         41.408
smc73-m02:     Total Transferred (MB):     10.125
smc73-m02:     Ttfb 90th-ile:              2.842
smc73-m02:     Ttfb 99th-ile:              4.729
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       155520
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1.082
smc73-m02:     Duration Max:               1.911
smc73-m02:     Duration Avg:               0.346
smc73-m02:     Duration Min:               0.021
smc73-m02:     Ttfb Max:                   1.911
smc73-m02:     Ttfb Avg:                   0.346
smc73-m02:     Ttfb Min:                   0.021
smc73-m02:     Duration 90th-ile:          0.403
smc73-m02:     Duration 99th-ile:          0.717
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         140.395
smc73-m02:     Total Transferred (MB):     151.875
smc73-m02:     Ttfb 90th-ile:              0.403
smc73-m02:     Ttfb 99th-ile:              0.717
```

## 10.9. 512 sessions

```
workload 16
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.001
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.247
smc73-m02:     Duration Max:               13.617
smc73-m02:     Duration Avg:               1.967
smc73-m02:     Duration Min:               0.417
smc73-m02:     Ttfb Max:                   13.617
smc73-m02:     Ttfb Avg:                   1.967
smc73-m02:     Ttfb Min:                   0.417
smc73-m02:     Duration 90th-ile:          3.954
smc73-m02:     Duration 99th-ile:          8.343
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         40.443
smc73-m02:     Total Transferred (MB):     10.000
smc73-m02:     Ttfb 90th-ile:              3.954
smc73-m02:     Ttfb 99th-ile:              8.343
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1.267
smc73-m02:     Duration Max:               1.979
smc73-m02:     Duration Avg:               0.394
smc73-m02:     Duration Min:               0.031
smc73-m02:     Ttfb Max:                   1.979
smc73-m02:     Ttfb Avg:                   0.394
smc73-m02:     Ttfb Min:                   0.031
smc73-m02:     Duration 90th-ile:          0.476
smc73-m02:     Duration 99th-ile:          0.736
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         118.416
smc73-m02:     Total Transferred (MB):     150.000
smc73-m02:     Ttfb 90th-ile:              0.476
smc73-m02:     Ttfb 99th-ile:              0.736
```

# 11. TTFB, 16 KB, 1-512 sessions

## 11.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 1
  batch_id: ttfb-v03-16Kb
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   256 -c   1 -o 16Kb -e 3 -- -sampleReads 40
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  16 -o 16Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  32 -o 16Kb -e 3 -- -sampleReads 20
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c  64 -o 16Kb -e 3 -- -sampleReads 25
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 128 -o 16Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 256 -o 16Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10368 -c 384 -o 16Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 512 -o 16Kb -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 11.2. 1 session

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 256
smc73-m02:     objectSize (MB):            0.016
smc73-m02:     sampleReads:                40
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.010
smc73-m02:     Duration Max:               2.245
smc73-m02:     Duration Avg:               1.559
smc73-m02:     Duration Min:               1.521
smc73-m02:     Ttfb Max:                   2.245
smc73-m02:     Ttfb Avg:                   1.559
smc73-m02:     Ttfb Min:                   1.521
smc73-m02:     Duration 90th-ile:          1.570
smc73-m02:     Duration 99th-ile:          2.142
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         399.087
smc73-m02:     Total Transferred (MB):     4.000
smc73-m02:     Ttfb 90th-ile:              1.570
smc73-m02:     Ttfb 99th-ile:              2.142
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.285
smc73-m02:     Duration Max:               0.291
smc73-m02:     Duration Avg:               0.055
smc73-m02:     Duration Min:               0.051
smc73-m02:     Ttfb Max:                   0.252
smc73-m02:     Ttfb Avg:                   0.015
smc73-m02:     Ttfb Min:                   0.011
smc73-m02:     Duration 90th-ile:          0.056
smc73-m02:     Duration 99th-ile:          0.080
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         561.221
smc73-m02:     Total Transferred (MB):     160.000
smc73-m02:     Ttfb 90th-ile:              0.017
smc73-m02:     Ttfb 99th-ile:              0.041
```

## 11.3. 16 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.016
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.174
smc73-m02:     Duration Max:               2.157
smc73-m02:     Duration Avg:               1.435
smc73-m02:     Duration Min:               0.639
smc73-m02:     Ttfb Max:                   2.157
smc73-m02:     Ttfb Avg:                   1.435
smc73-m02:     Ttfb Min:                   0.639
smc73-m02:     Duration 90th-ile:          1.534
smc73-m02:     Duration 99th-ile:          1.851
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         230.429
smc73-m02:     Total Transferred (MB):     40.000
smc73-m02:     Ttfb 90th-ile:              1.534
smc73-m02:     Ttfb 99th-ile:              1.851
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       38400
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3.736
smc73-m02:     Duration Max:               1.194
smc73-m02:     Duration Avg:               0.067
smc73-m02:     Duration Min:               0.011
smc73-m02:     Ttfb Max:                   1.154
smc73-m02:     Ttfb Avg:                   0.028
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.092
smc73-m02:     Duration 99th-ile:          0.295
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         160.587
smc73-m02:     Total Transferred (MB):     600.000
smc73-m02:     Ttfb 90th-ile:              0.053
smc73-m02:     Ttfb 99th-ile:              0.256
```

## 11.4. 32 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.016
smc73-m02:     sampleReads:                20
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.384
smc73-m02:     Duration Max:               1.887
smc73-m02:     Duration Avg:               1.292
smc73-m02:     Duration Min:               0.610
smc73-m02:     Ttfb Max:                   1.887
smc73-m02:     Ttfb Avg:                   1.292
smc73-m02:     Ttfb Min:                   0.610
smc73-m02:     Duration 90th-ile:          1.540
smc73-m02:     Duration 99th-ile:          1.596
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         104.193
smc73-m02:     Total Transferred (MB):     40.000
smc73-m02:     Ttfb 90th-ile:              1.540
smc73-m02:     Ttfb 99th-ile:              1.596
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6.905
smc73-m02:     Duration Max:               1.371
smc73-m02:     Duration Avg:               0.072
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   1.331
smc73-m02:     Ttfb Avg:                   0.035
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.108
smc73-m02:     Duration 99th-ile:          0.163
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         115.852
smc73-m02:     Total Transferred (MB):     800.000
smc73-m02:     Ttfb 90th-ile:              0.072
smc73-m02:     Ttfb 99th-ile:              0.126
```

## 11.5. 64 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            0.016
smc73-m02:     sampleReads:                25
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.751
smc73-m02:     Duration Max:               1.886
smc73-m02:     Duration Avg:               1.321
smc73-m02:     Duration Min:               0.625
smc73-m02:     Ttfb Max:                   1.886
smc73-m02:     Ttfb Avg:                   1.321
smc73-m02:     Ttfb Min:                   0.625
smc73-m02:     Duration 90th-ile:          1.557
smc73-m02:     Duration 99th-ile:          1.670
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         106.527
smc73-m02:     Total Transferred (MB):     80.000
smc73-m02:     Ttfb 90th-ile:              1.557
smc73-m02:     Ttfb 99th-ile:              1.670
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       128000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    12.322
smc73-m02:     Duration Max:               2.216
smc73-m02:     Duration Avg:               0.081
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   2.176
smc73-m02:     Ttfb Avg:                   0.046
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.120
smc73-m02:     Duration 99th-ile:          0.158
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         162.307
smc73-m02:     Total Transferred (MB):     2000.000
smc73-m02:     Ttfb 90th-ile:              0.082
smc73-m02:     Ttfb 99th-ile:              0.120
```

## 11.6. 128 sessions

```
workload 10
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.016
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1.528
smc73-m02:     Duration Max:               2.223
smc73-m02:     Duration Avg:               1.299
smc73-m02:     Duration Min:               0.489
smc73-m02:     Ttfb Max:                   2.223
smc73-m02:     Ttfb Avg:                   1.299
smc73-m02:     Ttfb Min:                   0.489
smc73-m02:     Duration 90th-ile:          1.612
smc73-m02:     Duration 99th-ile:          1.878
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         104.701
smc73-m02:     Total Transferred (MB):     160.000
smc73-m02:     Ttfb 90th-ile:              1.612
smc73-m02:     Ttfb 99th-ile:              1.878
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    18.936
smc73-m02:     Duration Max:               1.694
smc73-m02:     Duration Avg:               0.106
smc73-m02:     Duration Min:               0.012
smc73-m02:     Ttfb Max:                   1.655
smc73-m02:     Ttfb Avg:                   0.069
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.141
smc73-m02:     Duration 99th-ile:          0.217
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         126.746
smc73-m02:     Total Transferred (MB):     2400.000
smc73-m02:     Ttfb 90th-ile:              0.103
smc73-m02:     Ttfb 99th-ile:              0.181
```

## 11.7. 256 sessions

```
workload 12
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.016
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3.676
smc73-m02:     Duration Max:               4.220
smc73-m02:     Duration Avg:               1.047
smc73-m02:     Duration Min:               0.316
smc73-m02:     Ttfb Max:                   4.220
smc73-m02:     Ttfb Avg:                   1.047
smc73-m02:     Ttfb Min:                   0.316
smc73-m02:     Duration 90th-ile:          2.051
smc73-m02:     Duration 99th-ile:          2.888
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         43.530
smc73-m02:     Total Transferred (MB):     160.000
smc73-m02:     Ttfb 90th-ile:              2.051
smc73-m02:     Ttfb 99th-ile:              2.888
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    21.418
smc73-m02:     Duration Max:               1.360
smc73-m02:     Duration Avg:               0.187
smc73-m02:     Duration Min:               0.014
smc73-m02:     Ttfb Max:                   1.321
smc73-m02:     Ttfb Avg:                   0.151
smc73-m02:     Ttfb Min:                   0.011
smc73-m02:     Duration 90th-ile:          0.229
smc73-m02:     Duration 99th-ile:          0.380
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         112.054
smc73-m02:     Total Transferred (MB):     2400.000
smc73-m02:     Ttfb 90th-ile:              0.192
smc73-m02:     Ttfb 99th-ile:              0.345
```

## 11.8. 384 sessions

```
workload 14
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 10368
smc73-m02:     objectSize (MB):            0.016
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10368
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3.642
smc73-m02:     Duration Max:               11.370
smc73-m02:     Duration Avg:               1.611
smc73-m02:     Duration Min:               0.378
smc73-m02:     Ttfb Max:                   11.370
smc73-m02:     Ttfb Avg:                   1.611
smc73-m02:     Ttfb Min:                   0.378
smc73-m02:     Duration 90th-ile:          3.446
smc73-m02:     Duration 99th-ile:          6.921
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         44.477
smc73-m02:     Total Transferred (MB):     162.000
smc73-m02:     Ttfb 90th-ile:              3.446
smc73-m02:     Ttfb 99th-ile:              6.921
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       155520
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    18.048
smc73-m02:     Duration Max:               1.345
smc73-m02:     Duration Avg:               0.332
smc73-m02:     Duration Min:               0.029
smc73-m02:     Ttfb Max:                   1.305
smc73-m02:     Ttfb Avg:                   0.296
smc73-m02:     Ttfb Min:                   0.026
smc73-m02:     Duration 90th-ile:          0.381
smc73-m02:     Duration 99th-ile:          0.645
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         134.642
smc73-m02:     Total Transferred (MB):     2430.000
smc73-m02:     Ttfb 90th-ile:              0.344
smc73-m02:     Ttfb 99th-ile:              0.609
```

## 11.9. 512 sessions

```
workload 16
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.016
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3.651
smc73-m02:     Duration Max:               14.336
smc73-m02:     Duration Avg:               2.137
smc73-m02:     Duration Min:               0.423
smc73-m02:     Ttfb Max:                   14.336
smc73-m02:     Ttfb Avg:                   2.137
smc73-m02:     Ttfb Min:                   0.423
smc73-m02:     Duration 90th-ile:          4.210
smc73-m02:     Duration 99th-ile:          12.399
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         43.827
smc73-m02:     Total Transferred (MB):     160.000
smc73-m02:     Ttfb 90th-ile:              4.210
smc73-m02:     Ttfb 99th-ile:              12.399
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    11.539
smc73-m02:     Duration Max:               1.863
smc73-m02:     Duration Avg:               0.693
smc73-m02:     Duration Min:               0.018
smc73-m02:     Ttfb Max:                   1.823
smc73-m02:     Ttfb Avg:                   0.656
smc73-m02:     Ttfb Min:                   0.015
smc73-m02:     Duration 90th-ile:          0.788
smc73-m02:     Duration 99th-ile:          1.170
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         207.988
smc73-m02:     Total Transferred (MB):     2400.000
smc73-m02:     Ttfb 90th-ile:              0.751
smc73-m02:     Ttfb 99th-ile:              1.132
```


# 12. TTFB, 100 KB, 1-512 sessions

## 12.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 1
  batch_id: ttfb-v03-100Kb
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   256 -c   1 -o 100Kb -e 3 -- -sampleReads 40
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  16 -o 100Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  32 -o 100Kb -e 3 -- -sampleReads 20
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c  64 -o 100Kb -e 3 -- -sampleReads 25
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 128 -o 100Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 256 -o 100Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10368 -c 384 -o 100Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 512 -o 100Kb -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 12.2. 1 session

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 256
smc73-m02:     objectSize (MB):            0.098
smc73-m02:     sampleReads:                40
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.063
smc73-m02:     Duration Max:               2.161
smc73-m02:     Duration Avg:               1.562
smc73-m02:     Duration Min:               1.523
smc73-m02:     Ttfb Max:                   2.161
smc73-m02:     Ttfb Avg:                   1.562
smc73-m02:     Ttfb Min:                   1.523
smc73-m02:     Duration 90th-ile:          1.576
smc73-m02:     Duration 99th-ile:          1.872
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         399.944
smc73-m02:     Total Transferred (MB):     25.000
smc73-m02:     Ttfb 90th-ile:              1.576
smc73-m02:     Ttfb 99th-ile:              1.872
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3.772
smc73-m02:     Duration Max:               0.666
smc73-m02:     Duration Avg:               0.026
smc73-m02:     Duration Min:               0.011
smc73-m02:     Ttfb Max:                   0.665
smc73-m02:     Ttfb Avg:                   0.014
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.054
smc73-m02:     Duration 99th-ile:          0.062
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         265.094
smc73-m02:     Total Transferred (MB):     1000.000
smc73-m02:     Ttfb 90th-ile:              0.016
smc73-m02:     Ttfb 99th-ile:              0.031
```

## 12.3. 16 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.098
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1.105
smc73-m02:     Duration Max:               2.314
smc73-m02:     Duration Avg:               1.409
smc73-m02:     Duration Min:               0.507
smc73-m02:     Ttfb Max:                   2.314
smc73-m02:     Ttfb Avg:                   1.409
smc73-m02:     Ttfb Min:                   0.507
smc73-m02:     Duration 90th-ile:          1.533
smc73-m02:     Duration 99th-ile:          1.686
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         226.220
smc73-m02:     Total Transferred (MB):     250.000
smc73-m02:     Ttfb 90th-ile:              1.533
smc73-m02:     Ttfb 99th-ile:              1.686
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       38400
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    26.731
smc73-m02:     Duration Max:               1.048
smc73-m02:     Duration Avg:               0.058
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   1.008
smc73-m02:     Ttfb Avg:                   0.027
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.092
smc73-m02:     Duration 99th-ile:          0.208
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         140.285
smc73-m02:     Total Transferred (MB):     3750.000
smc73-m02:     Ttfb 90th-ile:              0.054
smc73-m02:     Ttfb 99th-ile:              0.173
```

## 12.4. 32 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.098
smc73-m02:     sampleReads:                20
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    2.486
smc73-m02:     Duration Max:               2.089
smc73-m02:     Duration Avg:               1.247
smc73-m02:     Duration Min:               0.620
smc73-m02:     Ttfb Max:                   2.089
smc73-m02:     Ttfb Avg:                   1.247
smc73-m02:     Ttfb Min:                   0.620
smc73-m02:     Duration 90th-ile:          1.537
smc73-m02:     Duration 99th-ile:          1.780
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         100.568
smc73-m02:     Total Transferred (MB):     250.000
smc73-m02:     Ttfb 90th-ile:              1.537
smc73-m02:     Ttfb 99th-ile:              1.780
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    46.282
smc73-m02:     Duration Max:               1.019
smc73-m02:     Duration Avg:               0.067
smc73-m02:     Duration Min:               0.009
smc73-m02:     Ttfb Max:                   0.979
smc73-m02:     Ttfb Avg:                   0.033
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.101
smc73-m02:     Duration 99th-ile:          0.162
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         108.034
smc73-m02:     Total Transferred (MB):     5000.000
smc73-m02:     Ttfb 90th-ile:              0.065
smc73-m02:     Ttfb 99th-ile:              0.126
```

## 12.5. 64 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            0.098
smc73-m02:     sampleReads:                25
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    4.562
smc73-m02:     Duration Max:               2.573
smc73-m02:     Duration Avg:               1.361
smc73-m02:     Duration Min:               0.625
smc73-m02:     Ttfb Max:                   2.573
smc73-m02:     Ttfb Avg:                   1.361
smc73-m02:     Ttfb Min:                   0.625
smc73-m02:     Duration 90th-ile:          1.561
smc73-m02:     Duration 99th-ile:          2.536
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         109.613
smc73-m02:     Total Transferred (MB):     500.000
smc73-m02:     Ttfb 90th-ile:              1.561
smc73-m02:     Ttfb 99th-ile:              2.536
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       128000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    75.771
smc73-m02:     Duration Max:               1.062
smc73-m02:     Duration Avg:               0.082
smc73-m02:     Duration Min:               0.009
smc73-m02:     Ttfb Max:                   1.022
smc73-m02:     Ttfb Avg:                   0.047
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.121
smc73-m02:     Duration 99th-ile:          0.168
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         164.970
smc73-m02:     Total Transferred (MB):     12500.000
smc73-m02:     Ttfb 90th-ile:              0.082
smc73-m02:     Ttfb 99th-ile:              0.130
```

## 12.6. 128 sessions

```
workload 10
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.098
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    9.306
smc73-m02:     Duration Max:               2.464
smc73-m02:     Duration Avg:               1.335
smc73-m02:     Duration Min:               0.428
smc73-m02:     Ttfb Max:                   2.464
smc73-m02:     Ttfb Avg:                   1.335
smc73-m02:     Ttfb Min:                   0.428
smc73-m02:     Duration 90th-ile:          1.609
smc73-m02:     Duration 99th-ile:          1.914
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         107.456
smc73-m02:     Total Transferred (MB):     1000.000
smc73-m02:     Ttfb 90th-ile:              1.609
smc73-m02:     Ttfb 99th-ile:              1.914
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    116.568
smc73-m02:     Duration Max:               0.769
smc73-m02:     Duration Avg:               0.107
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   0.729
smc73-m02:     Ttfb Avg:                   0.072
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.146
smc73-m02:     Duration 99th-ile:          0.211
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         128.680
smc73-m02:     Total Transferred (MB):     15000.000
smc73-m02:     Ttfb 90th-ile:              0.108
smc73-m02:     Ttfb 99th-ile:              0.173
```

## 12.7. 256 sessions

```
workload 12
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.098
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    22.280
smc73-m02:     Duration Max:               4.988
smc73-m02:     Duration Avg:               1.095
smc73-m02:     Duration Min:               0.304
smc73-m02:     Ttfb Max:                   4.988
smc73-m02:     Ttfb Avg:                   1.095
smc73-m02:     Ttfb Min:                   0.304
smc73-m02:     Duration 90th-ile:          2.084
smc73-m02:     Duration 99th-ile:          2.909
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         44.883
smc73-m02:     Total Transferred (MB):     1000.000
smc73-m02:     Ttfb 90th-ile:              2.084
smc73-m02:     Ttfb 99th-ile:              2.909
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    107.695
smc73-m02:     Duration Max:               2.138
smc73-m02:     Duration Avg:               0.232
smc73-m02:     Duration Min:               0.011
smc73-m02:     Ttfb Max:                   2.123
smc73-m02:     Ttfb Avg:                   0.197
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.287
smc73-m02:     Duration 99th-ile:          0.455
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         139.283
smc73-m02:     Total Transferred (MB):     15000.000
smc73-m02:     Ttfb 90th-ile:              0.250
smc73-m02:     Ttfb 99th-ile:              0.419
```

## 12.8. 384 sessions

```
workload 14
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 10368
smc73-m02:     objectSize (MB):            0.098
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10368
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    25.018
smc73-m02:     Duration Max:               6.363
smc73-m02:     Duration Avg:               1.456
smc73-m02:     Duration Min:               0.352
smc73-m02:     Ttfb Max:                   6.363
smc73-m02:     Ttfb Avg:                   1.456
smc73-m02:     Ttfb Min:                   0.352
smc73-m02:     Duration 90th-ile:          2.706
smc73-m02:     Duration 99th-ile:          4.107
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         40.470
smc73-m02:     Total Transferred (MB):     1012.500
smc73-m02:     Ttfb 90th-ile:              2.706
smc73-m02:     Ttfb 99th-ile:              4.107
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       155520
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    107.295
smc73-m02:     Duration Max:               1.855
smc73-m02:     Duration Avg:               0.349
smc73-m02:     Duration Min:               0.034
smc73-m02:     Ttfb Max:                   1.815
smc73-m02:     Ttfb Avg:                   0.313
smc73-m02:     Ttfb Min:                   0.013
smc73-m02:     Duration 90th-ile:          0.407
smc73-m02:     Duration 99th-ile:          0.719
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         141.549
smc73-m02:     Total Transferred (MB):     15187.500
smc73-m02:     Ttfb 90th-ile:              0.369
smc73-m02:     Ttfb 99th-ile:              0.682
```

## 12.9. 512 sessions

```
workload 16
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.098
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    22.077
smc73-m02:     Duration Max:               12.459
smc73-m02:     Duration Avg:               2.203
smc73-m02:     Duration Min:               0.414
smc73-m02:     Ttfb Max:                   12.459
smc73-m02:     Ttfb Avg:                   2.203
smc73-m02:     Ttfb Min:                   0.414
smc73-m02:     Duration 90th-ile:          4.800
smc73-m02:     Duration 99th-ile:          10.920
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         45.296
smc73-m02:     Total Transferred (MB):     1000.000
smc73-m02:     Ttfb 90th-ile:              4.800
smc73-m02:     Ttfb 99th-ile:              10.920
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    81.091
smc73-m02:     Duration Max:               2.449
smc73-m02:     Duration Avg:               0.616
smc73-m02:     Duration Min:               0.026
smc73-m02:     Ttfb Max:                   2.410
smc73-m02:     Ttfb Avg:                   0.581
smc73-m02:     Ttfb Min:                   0.026
smc73-m02:     Duration 90th-ile:          0.703
smc73-m02:     Duration 99th-ile:          1.083
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         184.977
smc73-m02:     Total Transferred (MB):     15000.000
smc73-m02:     Ttfb 90th-ile:              0.667
smc73-m02:     Ttfb 99th-ile:              1.047
```


# 13. TTFB, 256 KB, 1-512 sessions

## 13.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 5
  batch_id: ttfb-v03-256Kb
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   256 -c   1 -o 256Kb -e 3 -- -sampleReads 40
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  16 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  32 -o 256Kb -e 3 -- -sampleReads 20
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c  64 -o 256Kb -e 3 -- -sampleReads 25
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 128 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 256 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10368 -c 384 -o 256Kb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 512 -o 256Kb -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 13.2. 1 session

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 256
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                40
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.159
smc73-m02:     Duration Max:               2.205
smc73-m02:     Duration Avg:               1.567
smc73-m02:     Duration Min:               1.528
smc73-m02:     Ttfb Max:                   2.205
smc73-m02:     Ttfb Avg:                   1.567
smc73-m02:     Ttfb Min:                   1.528
smc73-m02:     Duration 90th-ile:          1.580
smc73-m02:     Duration 99th-ile:          2.151
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         401.266
smc73-m02:     Total Transferred (MB):     64.000
smc73-m02:     Ttfb 90th-ile:              1.580
smc73-m02:     Ttfb 99th-ile:              2.151
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6.538
smc73-m02:     Duration Max:               0.440
smc73-m02:     Duration Avg:               0.038
smc73-m02:     Duration Min:               0.012
smc73-m02:     Ttfb Max:                   0.401
smc73-m02:     Ttfb Avg:                   0.015
smc73-m02:     Ttfb Min:                   0.011
smc73-m02:     Duration 90th-ile:          0.056
smc73-m02:     Duration 99th-ile:          0.070
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         391.571
smc73-m02:     Total Transferred (MB):     2560.000
smc73-m02:     Ttfb 90th-ile:              0.017
smc73-m02:     Ttfb 99th-ile:              0.039
```

## 13.3. 16 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    2.862
smc73-m02:     Duration Max:               2.161
smc73-m02:     Duration Avg:               1.393
smc73-m02:     Duration Min:               0.625
smc73-m02:     Ttfb Max:                   2.161
smc73-m02:     Ttfb Avg:                   1.393
smc73-m02:     Ttfb Min:                   0.625
smc73-m02:     Duration 90th-ile:          1.535
smc73-m02:     Duration 99th-ile:          1.646
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         223.655
smc73-m02:     Total Transferred (MB):     640.000
smc73-m02:     Ttfb 90th-ile:              1.535
smc73-m02:     Ttfb 99th-ile:              1.646
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       38400
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    81.003
smc73-m02:     Duration Max:               0.637
smc73-m02:     Duration Avg:               0.049
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   0.597
smc73-m02:     Ttfb Avg:                   0.026
smc73-m02:     Ttfb Min:                   0.009
smc73-m02:     Duration 90th-ile:          0.082
smc73-m02:     Duration 99th-ile:          0.151
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         118.514
smc73-m02:     Total Transferred (MB):     9600.000
smc73-m02:     Ttfb 90th-ile:              0.053
smc73-m02:     Ttfb 99th-ile:              0.123
```

## 13.4. 32 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                20
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5.698
smc73-m02:     Duration Max:               1.921
smc73-m02:     Duration Avg:               1.395
smc73-m02:     Duration Min:               0.635
smc73-m02:     Ttfb Max:                   1.921
smc73-m02:     Ttfb Avg:                   1.395
smc73-m02:     Ttfb Min:                   0.635
smc73-m02:     Duration 90th-ile:          1.543
smc73-m02:     Duration 99th-ile:          1.849
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         112.318
smc73-m02:     Total Transferred (MB):     640.000
smc73-m02:     Ttfb 90th-ile:              1.543
smc73-m02:     Ttfb 99th-ile:              1.849
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    130.178
smc73-m02:     Duration Max:               1.196
smc73-m02:     Duration Avg:               0.061
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   1.157
smc73-m02:     Ttfb Avg:                   0.036
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.097
smc73-m02:     Duration 99th-ile:          0.169
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         98.327
smc73-m02:     Total Transferred (MB):     12800.000
smc73-m02:     Ttfb 90th-ile:              0.068
smc73-m02:     Ttfb 99th-ile:              0.138
```

## 13.5. 64 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                25
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    12.539
smc73-m02:     Duration Max:               2.348
smc73-m02:     Duration Avg:               1.266
smc73-m02:     Duration Min:               0.618
smc73-m02:     Ttfb Max:                   2.348
smc73-m02:     Ttfb Avg:                   1.266
smc73-m02:     Ttfb Min:                   0.618
smc73-m02:     Duration 90th-ile:          1.555
smc73-m02:     Duration 99th-ile:          1.684
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         102.080
smc73-m02:     Total Transferred (MB):     1280.000
smc73-m02:     Ttfb 90th-ile:              1.555
smc73-m02:     Ttfb 99th-ile:              1.684
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       128000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    218.853
smc73-m02:     Duration Max:               1.621
smc73-m02:     Duration Avg:               0.073
smc73-m02:     Duration Min:               0.010
smc73-m02:     Ttfb Max:                   1.583
smc73-m02:     Ttfb Avg:                   0.047
smc73-m02:     Ttfb Min:                   0.010
smc73-m02:     Duration 90th-ile:          0.110
smc73-m02:     Duration 99th-ile:          0.161
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         146.217
smc73-m02:     Total Transferred (MB):     32000.000
smc73-m02:     Ttfb 90th-ile:              0.078
smc73-m02:     Ttfb 99th-ile:              0.130
```

## 13.6. 128 sessions

```
workload 10
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    23.919
smc73-m02:     Duration Max:               2.817
smc73-m02:     Duration Avg:               1.327
smc73-m02:     Duration Min:               0.457
smc73-m02:     Ttfb Max:                   2.817
smc73-m02:     Ttfb Avg:                   1.327
smc73-m02:     Ttfb Min:                   0.457
smc73-m02:     Duration 90th-ile:          1.617
smc73-m02:     Duration 99th-ile:          1.918
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         107.027
smc73-m02:     Total Transferred (MB):     2560.000
smc73-m02:     Ttfb 90th-ile:              1.617
smc73-m02:     Ttfb 99th-ile:              1.918
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    307.442
smc73-m02:     Duration Max:               2.647
smc73-m02:     Duration Avg:               0.104
smc73-m02:     Duration Min:               0.011
smc73-m02:     Ttfb Max:                   2.607
smc73-m02:     Ttfb Avg:                   0.078
smc73-m02:     Ttfb Min:                   0.011
smc73-m02:     Duration 90th-ile:          0.143
smc73-m02:     Duration 99th-ile:          0.206
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         124.902
smc73-m02:     Total Transferred (MB):     38400.000
smc73-m02:     Ttfb 90th-ile:              0.111
smc73-m02:     Ttfb 99th-ile:              0.173
```

## 13.7. 256 sessions

```
workload 12
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    55.982
smc73-m02:     Duration Max:               4.357
smc73-m02:     Duration Avg:               1.126
smc73-m02:     Duration Min:               0.325
smc73-m02:     Ttfb Max:                   4.357
smc73-m02:     Ttfb Avg:                   1.126
smc73-m02:     Ttfb Min:                   0.325
smc73-m02:     Duration 90th-ile:          2.076
smc73-m02:     Duration 99th-ile:          3.024
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         45.729
smc73-m02:     Total Transferred (MB):     2560.000
smc73-m02:     Ttfb 90th-ile:              2.076
smc73-m02:     Ttfb 99th-ile:              3.024
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    382.258
smc73-m02:     Duration Max:               1.393
smc73-m02:     Duration Avg:               0.167
smc73-m02:     Duration Min:               0.021
smc73-m02:     Ttfb Max:                   1.353
smc73-m02:     Ttfb Avg:                   0.140
smc73-m02:     Ttfb Min:                   0.015
smc73-m02:     Duration 90th-ile:          0.210
smc73-m02:     Duration 99th-ile:          0.288
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         100.456
smc73-m02:     Total Transferred (MB):     38400.000
smc73-m02:     Ttfb 90th-ile:              0.177
smc73-m02:     Ttfb 99th-ile:              0.256
```

## 13.8. 384 sessions

```
workload 14
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 10368
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10368
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    54.315
smc73-m02:     Duration Max:               10.532
smc73-m02:     Duration Avg:               1.733
smc73-m02:     Duration Min:               0.399
smc73-m02:     Ttfb Max:                   10.532
smc73-m02:     Ttfb Avg:                   1.733
smc73-m02:     Ttfb Min:                   0.399
smc73-m02:     Duration 90th-ile:          3.106
smc73-m02:     Duration 99th-ile:          6.891
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         47.722
smc73-m02:     Total Transferred (MB):     2592.000
smc73-m02:     Ttfb 90th-ile:              3.106
smc73-m02:     Ttfb 99th-ile:              6.891
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       155520
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    236.850
smc73-m02:     Duration Max:               1.612
smc73-m02:     Duration Avg:               0.405
smc73-m02:     Duration Min:               0.021
smc73-m02:     Ttfb Max:                   1.572
smc73-m02:     Ttfb Avg:                   0.378
smc73-m02:     Ttfb Min:                   0.020
smc73-m02:     Duration 90th-ile:          0.478
smc73-m02:     Duration 99th-ile:          0.731
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         164.154
smc73-m02:     Total Transferred (MB):     38880.000
smc73-m02:     Ttfb 90th-ile:              0.448
smc73-m02:     Ttfb 99th-ile:              0.701
```

## 13.9. 512 sessions

```
workload 16
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            0.250
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    64.612
smc73-m02:     Duration Max:               11.616
smc73-m02:     Duration Avg:               1.926
smc73-m02:     Duration Min:               0.411
smc73-m02:     Ttfb Max:                   11.616
smc73-m02:     Ttfb Avg:                   1.926
smc73-m02:     Ttfb Min:                   0.411
smc73-m02:     Duration 90th-ile:          3.916
smc73-m02:     Duration 99th-ile:          8.155
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         39.621
smc73-m02:     Total Transferred (MB):     2560.000
smc73-m02:     Ttfb 90th-ile:              3.916
smc73-m02:     Ttfb 99th-ile:              8.155
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    230.609
smc73-m02:     Duration Max:               1.957
smc73-m02:     Duration Avg:               0.554
smc73-m02:     Duration Min:               0.023
smc73-m02:     Ttfb Max:                   1.956
smc73-m02:     Ttfb Avg:                   0.528
smc73-m02:     Ttfb Min:                   0.023
smc73-m02:     Duration 90th-ile:          0.610
smc73-m02:     Duration 99th-ile:          0.828
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         166.515
smc73-m02:     Total Transferred (MB):     38400.000
smc73-m02:     Ttfb 90th-ile:              0.577
smc73-m02:     Ttfb 99th-ile:              0.801
```


# 14. TTFB, 1 MB, 1-512 sessions

## 14.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 1
  batch_id: ttfb-v04-1Mb
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   256 -c   1 -o 1Mb -e 3 -- -sampleReads 40
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  16 -o 1Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  32 -o 1Mb -e 3 -- -sampleReads 20
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c  64 -o 1Mb -e 3 -- -sampleReads 25
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 128 -o 1Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 256 -o 1Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10368 -c 384 -o 1Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 512 -o 1Mb -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 14.2. 1 session

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 256
smc73-m02:     objectSize (MB):            1.000
smc73-m02:     sampleReads:                40
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    0.628
smc73-m02:     Duration Max:               2.332
smc73-m02:     Duration Avg:               1.593
smc73-m02:     Duration Min:               1.545
smc73-m02:     Ttfb Max:                   2.332
smc73-m02:     Ttfb Avg:                   1.593
smc73-m02:     Ttfb Min:                   1.545
smc73-m02:     Duration 90th-ile:          1.630
smc73-m02:     Duration 99th-ile:          2.182
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         407.860
smc73-m02:     Total Transferred (MB):     256.000
smc73-m02:     Ttfb 90th-ile:              1.630
smc73-m02:     Ttfb 99th-ile:              2.182
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    20.271
smc73-m02:     Duration Max:               0.771
smc73-m02:     Duration Avg:               0.049
smc73-m02:     Duration Min:               0.013
smc73-m02:     Ttfb Max:                   0.731
smc73-m02:     Ttfb Avg:                   0.018
smc73-m02:     Ttfb Min:                   0.013
smc73-m02:     Duration 90th-ile:          0.059
smc73-m02:     Duration 99th-ile:          0.098
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         505.150
smc73-m02:     Total Transferred (MB):     10240.000
smc73-m02:     Ttfb 90th-ile:              0.020
smc73-m02:     Ttfb 99th-ile:              0.059
```

## 14.3. 16 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            1.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    11.735
smc73-m02:     Duration Max:               1.889
smc73-m02:     Duration Avg:               1.356
smc73-m02:     Duration Min:               0.684
smc73-m02:     Ttfb Max:                   1.889
smc73-m02:     Ttfb Avg:                   1.356
smc73-m02:     Ttfb Min:                   0.684
smc73-m02:     Duration 90th-ile:          1.551
smc73-m02:     Duration 99th-ile:          1.852
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         218.145
smc73-m02:     Total Transferred (MB):     2560.000
smc73-m02:     Ttfb 90th-ile:              1.551
smc73-m02:     Ttfb 99th-ile:              1.852
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       38400
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    302.629
smc73-m02:     Duration Max:               0.870
smc73-m02:     Duration Avg:               0.053
smc73-m02:     Duration Min:               0.012
smc73-m02:     Ttfb Max:                   0.830
smc73-m02:     Ttfb Avg:                   0.024
smc73-m02:     Ttfb Min:                   0.011
smc73-m02:     Duration 90th-ile:          0.080
smc73-m02:     Duration 99th-ile:          0.133
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         126.888
smc73-m02:     Total Transferred (MB):     38400.000
smc73-m02:     Ttfb 90th-ile:              0.050
smc73-m02:     Ttfb 99th-ile:              0.096
```

## 14.4. 32 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            1.000
smc73-m02:     sampleReads:                20
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    23.664
smc73-m02:     Duration Max:               2.176
smc73-m02:     Duration Avg:               1.344
smc73-m02:     Duration Min:               0.654
smc73-m02:     Ttfb Max:                   2.176
smc73-m02:     Ttfb Avg:                   1.344
smc73-m02:     Ttfb Min:                   0.654
smc73-m02:     Duration 90th-ile:          1.552
smc73-m02:     Duration 99th-ile:          1.759
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         108.180
smc73-m02:     Total Transferred (MB):     2560.000
smc73-m02:     Ttfb 90th-ile:              1.552
smc73-m02:     Ttfb 99th-ile:              1.759
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    501.117
smc73-m02:     Duration Max:               0.765
smc73-m02:     Duration Avg:               0.064
smc73-m02:     Duration Min:               0.012
smc73-m02:     Ttfb Max:                   0.725
smc73-m02:     Ttfb Avg:                   0.036
smc73-m02:     Ttfb Min:                   0.011
smc73-m02:     Duration 90th-ile:          0.101
smc73-m02:     Duration 99th-ile:          0.164
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         102.172
smc73-m02:     Total Transferred (MB):     51200.000
smc73-m02:     Ttfb 90th-ile:              0.070
smc73-m02:     Ttfb 99th-ile:              0.129
```

## 14.5. 64 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            1.000
smc73-m02:     sampleReads:                25
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    47.372
smc73-m02:     Duration Max:               2.405
smc73-m02:     Duration Avg:               1.339
smc73-m02:     Duration Min:               0.617
smc73-m02:     Ttfb Max:                   2.405
smc73-m02:     Ttfb Avg:                   1.339
smc73-m02:     Ttfb Min:                   0.617
smc73-m02:     Duration 90th-ile:          1.581
smc73-m02:     Duration 99th-ile:          2.002
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         108.082
smc73-m02:     Total Transferred (MB):     5120.000
smc73-m02:     Ttfb 90th-ile:              1.581
smc73-m02:     Ttfb 99th-ile:              2.002
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       128000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    807.401
smc73-m02:     Duration Max:               1.431
smc73-m02:     Duration Avg:               0.079
smc73-m02:     Duration Min:               0.012
smc73-m02:     Ttfb Max:                   1.392
smc73-m02:     Ttfb Avg:                   0.052
smc73-m02:     Ttfb Min:                   0.011
smc73-m02:     Duration 90th-ile:          0.121
smc73-m02:     Duration 99th-ile:          0.177
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         158.533
smc73-m02:     Total Transferred (MB):     128000.000
smc73-m02:     Ttfb 90th-ile:              0.088
smc73-m02:     Ttfb 99th-ile:              0.142
```

## 14.6. 128 sessions

```
workload 10
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            1.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    92.679
smc73-m02:     Duration Max:               2.889
smc73-m02:     Duration Avg:               1.371
smc73-m02:     Duration Min:               0.545
smc73-m02:     Ttfb Max:                   2.889
smc73-m02:     Ttfb Avg:                   1.371
smc73-m02:     Ttfb Min:                   0.545
smc73-m02:     Duration 90th-ile:          1.623
smc73-m02:     Duration 99th-ile:          1.938
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         110.489
smc73-m02:     Total Transferred (MB):     10240.000
smc73-m02:     Ttfb 90th-ile:              1.623
smc73-m02:     Ttfb 99th-ile:              1.938
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1199.283
smc73-m02:     Duration Max:               1.253
smc73-m02:     Duration Avg:               0.107
smc73-m02:     Duration Min:               0.013
smc73-m02:     Ttfb Max:                   1.219
smc73-m02:     Ttfb Avg:                   0.078
smc73-m02:     Ttfb Min:                   0.012
smc73-m02:     Duration 90th-ile:          0.153
smc73-m02:     Duration 99th-ile:          0.247
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         128.077
smc73-m02:     Total Transferred (MB):     153600.000
smc73-m02:     Ttfb 90th-ile:              0.120
smc73-m02:     Ttfb 99th-ile:              0.213
```

## 14.7. 256 sessions

```
workload 12
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            1.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    219.594
smc73-m02:     Duration Max:               4.832
smc73-m02:     Duration Avg:               1.141
smc73-m02:     Duration Min:               0.361
smc73-m02:     Ttfb Max:                   4.832
smc73-m02:     Ttfb Avg:                   1.141
smc73-m02:     Ttfb Min:                   0.361
smc73-m02:     Duration 90th-ile:          2.344
smc73-m02:     Duration 99th-ile:          3.736
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         46.631
smc73-m02:     Total Transferred (MB):     10240.000
smc73-m02:     Ttfb 90th-ile:              2.344
smc73-m02:     Ttfb 99th-ile:              3.736
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1059.566
smc73-m02:     Duration Max:               1.040
smc73-m02:     Duration Avg:               0.241
smc73-m02:     Duration Min:               0.018
smc73-m02:     Ttfb Max:                   1.000
smc73-m02:     Ttfb Avg:                   0.213
smc73-m02:     Ttfb Min:                   0.014
smc73-m02:     Duration 90th-ile:          0.313
smc73-m02:     Duration 99th-ile:          0.571
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         144.965
smc73-m02:     Total Transferred (MB):     153600.000
smc73-m02:     Ttfb 90th-ile:              0.281
smc73-m02:     Ttfb 99th-ile:              0.542
```

## 14.8. 384 sessions

```
workload 14
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 10368
smc73-m02:     objectSize (MB):            1.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10368
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    248.196
smc73-m02:     Duration Max:               7.935
smc73-m02:     Duration Avg:               1.511
smc73-m02:     Duration Min:               0.483
smc73-m02:     Ttfb Max:                   7.935
smc73-m02:     Ttfb Avg:                   1.511
smc73-m02:     Ttfb Min:                   0.483
smc73-m02:     Duration 90th-ile:          2.740
smc73-m02:     Duration 99th-ile:          6.122
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         41.773
smc73-m02:     Total Transferred (MB):     10368.000
smc73-m02:     Ttfb 90th-ile:              2.740
smc73-m02:     Ttfb 99th-ile:              6.122
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       155520
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1386.432
smc73-m02:     Duration Max:               1.540
smc73-m02:     Duration Avg:               0.277
smc73-m02:     Duration Min:               0.032
smc73-m02:     Ttfb Max:                   1.500
smc73-m02:     Ttfb Avg:                   0.248
smc73-m02:     Ttfb Min:                   0.031
smc73-m02:     Duration 90th-ile:          0.340
smc73-m02:     Duration 99th-ile:          0.595
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         112.173
smc73-m02:     Total Transferred (MB):     155520.000
smc73-m02:     Ttfb 90th-ile:              0.307
smc73-m02:     Ttfb 99th-ile:              0.566
```

## 14.9. 512 sessions

```
workload 16
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            1.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    220.506
smc73-m02:     Duration Max:               12.229
smc73-m02:     Duration Avg:               2.263
smc73-m02:     Duration Min:               0.428
smc73-m02:     Ttfb Max:                   12.229
smc73-m02:     Ttfb Avg:                   2.263
smc73-m02:     Ttfb Min:                   0.428
smc73-m02:     Duration 90th-ile:          5.076
smc73-m02:     Duration 99th-ile:          8.009
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         46.439
smc73-m02:     Total Transferred (MB):     10240.000
smc73-m02:     Ttfb 90th-ile:              5.076
smc73-m02:     Ttfb 99th-ile:              8.009
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1006.755
smc73-m02:     Duration Max:               2.466
smc73-m02:     Duration Avg:               0.508
smc73-m02:     Duration Min:               0.051
smc73-m02:     Ttfb Max:                   2.465
smc73-m02:     Ttfb Avg:                   0.479
smc73-m02:     Ttfb Min:                   0.049
smc73-m02:     Duration 90th-ile:          0.571
smc73-m02:     Duration 99th-ile:          0.916
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         152.569
smc73-m02:     Total Transferred (MB):     153600.000
smc73-m02:     Ttfb 90th-ile:              0.538
smc73-m02:     Ttfb 99th-ile:              0.887
```


# 15. TTFB, 5 MB, 1-512 sessions

## 15.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 1
  batch_id: ttfb-v04-5Mb
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   256 -c   1 -o 5Mb -e 3 -- -sampleReads 40
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  16 -o 5Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2560 -c  32 -o 5Mb -e 3 -- -sampleReads 20
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c  64 -o 5Mb -e 3 -- -sampleReads 25
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 128 -o 5Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 256 -o 5Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10368 -c 384 -o 5Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 512 -o 5Mb -e 3 -- -sampleReads 15

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 15.2. 1 session

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 256
smc73-m02:     objectSize (MB):            5.000
smc73-m02:     sampleReads:                40
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       256
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3.075
smc73-m02:     Duration Max:               2.249
smc73-m02:     Duration Avg:               1.626
smc73-m02:     Duration Min:               1.578
smc73-m02:     Ttfb Max:                   2.249
smc73-m02:     Ttfb Avg:                   1.626
smc73-m02:     Ttfb Min:                   1.578
smc73-m02:     Duration 90th-ile:          1.639
smc73-m02:     Duration 99th-ile:          2.210
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         416.286
smc73-m02:     Total Transferred (MB):     1280.000
smc73-m02:     Ttfb 90th-ile:              1.639
smc73-m02:     Ttfb 99th-ile:              2.210
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    86.855
smc73-m02:     Duration Max:               0.878
smc73-m02:     Duration Avg:               0.058
smc73-m02:     Duration Min:               0.023
smc73-m02:     Ttfb Max:                   0.875
smc73-m02:     Ttfb Avg:                   0.025
smc73-m02:     Ttfb Min:                   0.020
smc73-m02:     Duration 90th-ile:          0.068
smc73-m02:     Duration 99th-ile:          0.090
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         589.490
smc73-m02:     Total Transferred (MB):     51200.000
smc73-m02:     Ttfb 90th-ile:              0.027
smc73-m02:     Ttfb 99th-ile:              0.052
```

## 15.3. 16 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            5.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    60.225
smc73-m02:     Duration Max:               2.321
smc73-m02:     Duration Avg:               1.325
smc73-m02:     Duration Min:               0.635
smc73-m02:     Ttfb Max:                   2.321
smc73-m02:     Ttfb Avg:                   1.325
smc73-m02:     Ttfb Min:                   0.635
smc73-m02:     Duration 90th-ile:          1.591
smc73-m02:     Duration 99th-ile:          1.900
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         212.535
smc73-m02:     Total Transferred (MB):     12800.000
smc73-m02:     Ttfb 90th-ile:              1.591
smc73-m02:     Ttfb 99th-ile:              1.900
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       38400
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1273.156
smc73-m02:     Duration Max:               1.021
smc73-m02:     Duration Avg:               0.063
smc73-m02:     Duration Min:               0.020
smc73-m02:     Ttfb Max:                   0.980
smc73-m02:     Ttfb Avg:                   0.035
smc73-m02:     Ttfb Min:                   0.017
smc73-m02:     Duration 90th-ile:          0.089
smc73-m02:     Duration 99th-ile:          0.163
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         150.806
smc73-m02:     Total Transferred (MB):     192000.000
smc73-m02:     Ttfb 90th-ile:              0.059
smc73-m02:     Ttfb 99th-ile:              0.133
```

## 15.4. 32 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 2560
smc73-m02:     objectSize (MB):            5.000
smc73-m02:     sampleReads:                20
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2560
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    116.496
smc73-m02:     Duration Max:               2.848
smc73-m02:     Duration Avg:               1.360
smc73-m02:     Duration Min:               0.660
smc73-m02:     Ttfb Max:                   2.848
smc73-m02:     Ttfb Avg:                   1.360
smc73-m02:     Ttfb Min:                   0.660
smc73-m02:     Duration 90th-ile:          1.601
smc73-m02:     Duration 99th-ile:          1.904
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         109.875
smc73-m02:     Total Transferred (MB):     12800.000
smc73-m02:     Ttfb 90th-ile:              1.601
smc73-m02:     Ttfb 99th-ile:              1.904
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    2130.369
smc73-m02:     Duration Max:               3.992
smc73-m02:     Duration Avg:               0.075
smc73-m02:     Duration Min:               0.021
smc73-m02:     Ttfb Max:                   3.976
smc73-m02:     Ttfb Avg:                   0.051
smc73-m02:     Ttfb Min:                   0.018
smc73-m02:     Duration 90th-ile:          0.113
smc73-m02:     Duration 99th-ile:          0.201
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         120.167
smc73-m02:     Total Transferred (MB):     256000.000
smc73-m02:     Ttfb 90th-ile:              0.082
smc73-m02:     Ttfb 99th-ile:              0.172
```

## 15.5. 64 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            5.000
smc73-m02:     sampleReads:                25
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    221.343
smc73-m02:     Duration Max:               3.880
smc73-m02:     Duration Avg:               1.435
smc73-m02:     Duration Min:               0.685
smc73-m02:     Ttfb Max:                   3.880
smc73-m02:     Ttfb Avg:                   1.435
smc73-m02:     Ttfb Min:                   0.685
smc73-m02:     Duration 90th-ile:          1.617
smc73-m02:     Duration 99th-ile:          1.963
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         115.657
smc73-m02:     Total Transferred (MB):     25600.000
smc73-m02:     Ttfb 90th-ile:              1.617
smc73-m02:     Ttfb 99th-ile:              1.963
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       128000
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3121.723
smc73-m02:     Duration Max:               1.200
smc73-m02:     Duration Avg:               0.102
smc73-m02:     Duration Min:               0.023
smc73-m02:     Ttfb Max:                   1.158
smc73-m02:     Ttfb Avg:                   0.076
smc73-m02:     Ttfb Min:                   0.018
smc73-m02:     Duration 90th-ile:          0.147
smc73-m02:     Duration 99th-ile:          0.222
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         205.015
smc73-m02:     Total Transferred (MB):     640000.000
smc73-m02:     Ttfb 90th-ile:              0.114
smc73-m02:     Ttfb 99th-ile:              0.190
```

## 15.6. 128 sessions

```
workload 10
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            5.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    673.000
smc73-m02:     Duration Max:               5.227
smc73-m02:     Duration Avg:               0.941
smc73-m02:     Duration Min:               0.428
smc73-m02:     Ttfb Max:                   5.227
smc73-m02:     Ttfb Avg:                   0.941
smc73-m02:     Ttfb Min:                   0.428
smc73-m02:     Duration 90th-ile:          1.260
smc73-m02:     Duration 99th-ile:          4.051
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         76.077
smc73-m02:     Total Transferred (MB):     51200.000
smc73-m02:     Ttfb 90th-ile:              1.260
smc73-m02:     Ttfb 99th-ile:              4.051
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    4466.191
smc73-m02:     Duration Max:               3.390
smc73-m02:     Duration Avg:               0.143
smc73-m02:     Duration Min:               0.027
smc73-m02:     Ttfb Max:                   3.347
smc73-m02:     Ttfb Avg:                   0.117
smc73-m02:     Ttfb Min:                   0.020
smc73-m02:     Duration 90th-ile:          0.193
smc73-m02:     Duration 99th-ile:          0.402
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         171.959
smc73-m02:     Total Transferred (MB):     768000.000
smc73-m02:     Ttfb 90th-ile:              0.160
smc73-m02:     Ttfb 99th-ile:              0.374
```

## 15.7. 256 sessions

```
workload 12
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            5.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    710.619
smc73-m02:     Duration Max:               7.820
smc73-m02:     Duration Avg:               1.776
smc73-m02:     Duration Min:               0.528
smc73-m02:     Ttfb Max:                   7.820
smc73-m02:     Ttfb Avg:                   1.776
smc73-m02:     Ttfb Min:                   0.528
smc73-m02:     Duration 90th-ile:          4.331
smc73-m02:     Duration 99th-ile:          5.415
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         72.050
smc73-m02:     Total Transferred (MB):     51200.000
smc73-m02:     Ttfb 90th-ile:              4.331
smc73-m02:     Ttfb 99th-ile:              5.415
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5254.152
smc73-m02:     Duration Max:               3.623
smc73-m02:     Duration Avg:               0.243
smc73-m02:     Duration Min:               0.029
smc73-m02:     Ttfb Max:                   3.573
smc73-m02:     Ttfb Avg:                   0.216
smc73-m02:     Ttfb Min:                   0.025
smc73-m02:     Duration 90th-ile:          0.319
smc73-m02:     Duration 99th-ile:          0.539
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         146.170
smc73-m02:     Total Transferred (MB):     768000.000
smc73-m02:     Ttfb 90th-ile:              0.288
smc73-m02:     Ttfb 99th-ile:              0.511
```

## 15.8. 384 sessions

```
workload 14
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 10368
smc73-m02:     objectSize (MB):            5.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10368
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    922.888
smc73-m02:     Duration Max:               8.064
smc73-m02:     Duration Avg:               2.039
smc73-m02:     Duration Min:               0.516
smc73-m02:     Ttfb Max:                   8.064
smc73-m02:     Ttfb Avg:                   2.039
smc73-m02:     Ttfb Min:                   0.516
smc73-m02:     Duration 90th-ile:          4.083
smc73-m02:     Duration 99th-ile:          6.174
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         56.171
smc73-m02:     Total Transferred (MB):     51840.000
smc73-m02:     Ttfb 90th-ile:              4.083
smc73-m02:     Ttfb 99th-ile:              6.174
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       155520
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    4667.947
smc73-m02:     Duration Max:               2.400
smc73-m02:     Duration Avg:               0.411
smc73-m02:     Duration Min:               0.040
smc73-m02:     Ttfb Max:                   2.357
smc73-m02:     Ttfb Avg:                   0.383
smc73-m02:     Ttfb Min:                   0.021
smc73-m02:     Duration 90th-ile:          0.520
smc73-m02:     Duration 99th-ile:          0.861
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         166.583
smc73-m02:     Total Transferred (MB):     777600.000
smc73-m02:     Ttfb 90th-ile:              0.489
smc73-m02:     Ttfb 99th-ile:              0.826
```

## 15.9. 512 sessions

```
workload 16
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            5.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    907.484
smc73-m02:     Duration Max:               16.383
smc73-m02:     Duration Avg:               2.760
smc73-m02:     Duration Min:               0.508
smc73-m02:     Ttfb Max:                   16.383
smc73-m02:     Ttfb Avg:                   2.760
smc73-m02:     Ttfb Min:                   0.508
smc73-m02:     Duration 90th-ile:          5.841
smc73-m02:     Duration 99th-ile:          10.523
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         56.420
smc73-m02:     Total Transferred (MB):     51200.000
smc73-m02:     Ttfb 90th-ile:              5.841
smc73-m02:     Ttfb 99th-ile:              10.523
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       153600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    4862.204
smc73-m02:     Duration Max:               3.484
smc73-m02:     Duration Avg:               0.525
smc73-m02:     Duration Min:               0.077
smc73-m02:     Ttfb Max:                   3.474
smc73-m02:     Ttfb Avg:                   0.496
smc73-m02:     Ttfb Min:                   0.074
smc73-m02:     Duration 90th-ile:          0.684
smc73-m02:     Duration 99th-ile:          1.087
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         157.953
smc73-m02:     Total Transferred (MB):     768000.000
smc73-m02:     Ttfb 90th-ile:              0.653
smc73-m02:     Ttfb 99th-ile:              1.055
```


# 16. TTFB, 16 MB, 1-512 sessions

## 16.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 5
  batch_id: ttfb-v03-16Mb
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n    32 -c   1 -o 16Mb -e 3 -- -sampleReads 40
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   448 -c  16 -o 16Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   896 -c  32 -o 16Mb -e 3 -- -sampleReads 15
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c  64 -o 16Mb -e 3 -- -sampleReads  6
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  7680 -c 128 -o 16Mb -e 3 -- -sampleReads  4
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 256 -o 16Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10368 -c 384 -o 16Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 10240 -c 512 -o 16Mb -e 3 -- -sampleReads  5

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 16.2. 1 session

```
workload 2
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 32
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                40
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       32
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    8.661
smc73-m02:     Duration Max:               2.683
smc73-m02:     Duration Avg:               1.847
smc73-m02:     Duration Min:               1.684
smc73-m02:     Ttfb Max:                   2.683
smc73-m02:     Ttfb Avg:                   1.847
smc73-m02:     Ttfb Min:                   1.684
smc73-m02:     Duration 90th-ile:          2.056
smc73-m02:     Duration 99th-ile:          2.683
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         59.115
smc73-m02:     Total Transferred (MB):     512.000
smc73-m02:     Ttfb 90th-ile:              2.056
smc73-m02:     Ttfb 99th-ile:              2.683
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       1280
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    224.671
smc73-m02:     Duration Max:               0.460
smc73-m02:     Duration Avg:               0.071
smc73-m02:     Duration Min:               0.041
smc73-m02:     Ttfb Max:                   0.412
smc73-m02:     Ttfb Avg:                   0.037
smc73-m02:     Ttfb Min:                   0.032
smc73-m02:     Duration 90th-ile:          0.086
smc73-m02:     Duration 99th-ile:          0.117
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         91.156
smc73-m02:     Total Transferred (MB):     20480.000
smc73-m02:     Ttfb 90th-ile:              0.040
smc73-m02:     Ttfb 99th-ile:              0.067
```

## 16.3. 16 sessions

```
workload 4
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 448
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       448
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    182.070
smc73-m02:     Duration Max:               2.131
smc73-m02:     Duration Avg:               1.378
smc73-m02:     Duration Min:               0.697
smc73-m02:     Ttfb Max:                   2.131
smc73-m02:     Ttfb Avg:                   1.378
smc73-m02:     Ttfb Min:                   0.697
smc73-m02:     Duration 90th-ile:          1.683
smc73-m02:     Duration 99th-ile:          1.829
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         39.370
smc73-m02:     Total Transferred (MB):     7168.000
smc73-m02:     Ttfb 90th-ile:              1.683
smc73-m02:     Ttfb 99th-ile:              1.829
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       6720
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3648.318
smc73-m02:     Duration Max:               0.415
smc73-m02:     Duration Avg:               0.070
smc73-m02:     Duration Min:               0.041
smc73-m02:     Ttfb Max:                   0.392
smc73-m02:     Ttfb Avg:                   0.049
smc73-m02:     Ttfb Min:                   0.031
smc73-m02:     Duration 90th-ile:          0.100
smc73-m02:     Duration 99th-ile:          0.163
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         29.471
smc73-m02:     Total Transferred (MB):     107520.000
smc73-m02:     Ttfb 90th-ile:              0.074
smc73-m02:     Ttfb 99th-ile:              0.133
```

## 16.4. 32 sessions

```
workload 6
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 896
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                15
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       896
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    347.868
smc73-m02:     Duration Max:               2.535
smc73-m02:     Duration Avg:               1.451
smc73-m02:     Duration Min:               0.887
smc73-m02:     Ttfb Max:                   2.535
smc73-m02:     Ttfb Avg:                   1.451
smc73-m02:     Ttfb Min:                   0.887
smc73-m02:     Duration 90th-ile:          1.718
smc73-m02:     Duration 99th-ile:          2.373
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         41.211
smc73-m02:     Total Transferred (MB):     14336.000
smc73-m02:     Ttfb 90th-ile:              1.718
smc73-m02:     Ttfb 99th-ile:              2.373
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       13440
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3973.183
smc73-m02:     Duration Max:               5.692
smc73-m02:     Duration Avg:               0.124
smc73-m02:     Duration Min:               0.045
smc73-m02:     Ttfb Max:                   5.645
smc73-m02:     Ttfb Avg:                   0.095
smc73-m02:     Ttfb Min:                   0.034
smc73-m02:     Duration 90th-ile:          0.150
smc73-m02:     Duration 99th-ile:          0.643
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         54.123
smc73-m02:     Total Transferred (MB):     215040.000
smc73-m02:     Ttfb 90th-ile:              0.111
smc73-m02:     Ttfb 99th-ile:              0.578
```

## 16.5. 64 sessions

```
workload 8
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                6
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    767.601
smc73-m02:     Duration Max:               5.151
smc73-m02:     Duration Avg:               1.324
smc73-m02:     Duration Min:               0.708
smc73-m02:     Ttfb Max:                   5.151
smc73-m02:     Ttfb Avg:                   1.324
smc73-m02:     Ttfb Min:                   0.708
smc73-m02:     Duration 90th-ile:          1.579
smc73-m02:     Duration 99th-ile:          2.274
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         106.722
smc73-m02:     Total Transferred (MB):     81920.000
smc73-m02:     Ttfb 90th-ile:              1.579
smc73-m02:     Ttfb 99th-ile:              2.274
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       30720
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6033.687
smc73-m02:     Duration Max:               4.176
smc73-m02:     Duration Avg:               0.169
smc73-m02:     Duration Min:               0.049
smc73-m02:     Ttfb Max:                   4.142
smc73-m02:     Ttfb Avg:                   0.146
smc73-m02:     Ttfb Min:                   0.038
smc73-m02:     Duration 90th-ile:          0.230
smc73-m02:     Duration 99th-ile:          0.495
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         81.463
smc73-m02:     Total Transferred (MB):     491520.000
smc73-m02:     Ttfb 90th-ile:              0.204
smc73-m02:     Ttfb 99th-ile:              0.471
```

## 16.6. 128 sessions

```
workload 10
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 7680
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                4
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       7680
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1329.137
smc73-m02:     Duration Max:               5.797
smc73-m02:     Duration Avg:               1.524
smc73-m02:     Duration Min:               0.604
smc73-m02:     Ttfb Max:                   5.797
smc73-m02:     Ttfb Avg:                   1.524
smc73-m02:     Ttfb Min:                   0.604
smc73-m02:     Duration 90th-ile:          3.767
smc73-m02:     Duration 99th-ile:          5.227
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         92.451
smc73-m02:     Total Transferred (MB):     122880.000
smc73-m02:     Ttfb 90th-ile:              3.767
smc73-m02:     Ttfb 99th-ile:              5.227
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       30720
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5934.462
smc73-m02:     Duration Max:               4.786
smc73-m02:     Duration Avg:               0.345
smc73-m02:     Duration Min:               0.047
smc73-m02:     Ttfb Max:                   4.522
smc73-m02:     Ttfb Avg:                   0.187
smc73-m02:     Ttfb Min:                   0.037
smc73-m02:     Duration 90th-ile:          0.496
smc73-m02:     Duration 99th-ile:          0.906
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         82.825
smc73-m02:     Total Transferred (MB):     491520.000
smc73-m02:     Ttfb 90th-ile:              0.273
smc73-m02:     Ttfb 99th-ile:              0.784
```

## 16.7. 256 sessions

```
workload 12
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1501.426
smc73-m02:     Duration Max:               13.175
smc73-m02:     Duration Avg:               2.690
smc73-m02:     Duration Min:               0.634
smc73-m02:     Ttfb Max:                   13.175
smc73-m02:     Ttfb Avg:                   2.690
smc73-m02:     Ttfb Min:                   0.634
smc73-m02:     Duration 90th-ile:          5.212
smc73-m02:     Duration 99th-ile:          8.903
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         109.123
smc73-m02:     Total Transferred (MB):     163840.000
smc73-m02:     Ttfb 90th-ile:              5.212
smc73-m02:     Ttfb 99th-ile:              8.903
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6787.470
smc73-m02:     Duration Max:               4.753
smc73-m02:     Duration Avg:               0.601
smc73-m02:     Duration Min:               0.050
smc73-m02:     Ttfb Max:                   4.447
smc73-m02:     Ttfb Avg:                   0.524
smc73-m02:     Ttfb Min:                   0.039
smc73-m02:     Duration 90th-ile:          1.617
smc73-m02:     Duration 99th-ile:          2.476
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         120.693
smc73-m02:     Total Transferred (MB):     819200.000
smc73-m02:     Ttfb 90th-ile:              1.544
smc73-m02:     Ttfb 99th-ile:              2.410
```

## 16.8. 384 sessions

```
workload 14
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 10368
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10368
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1717.495
smc73-m02:     Duration Max:               16.451
smc73-m02:     Duration Avg:               3.515
smc73-m02:     Duration Min:               0.654
smc73-m02:     Ttfb Max:                   16.451
smc73-m02:     Ttfb Avg:                   3.515
smc73-m02:     Ttfb Min:                   0.654
smc73-m02:     Duration 90th-ile:          8.019
smc73-m02:     Duration 99th-ile:          11.671
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         96.587
smc73-m02:     Total Transferred (MB):     165888.000
smc73-m02:     Ttfb 90th-ile:              8.019
smc73-m02:     Ttfb 99th-ile:              11.671
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51840
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    8671.294
smc73-m02:     Duration Max:               2.731
smc73-m02:     Duration Avg:               0.703
smc73-m02:     Duration Min:               0.108
smc73-m02:     Ttfb Max:                   2.581
smc73-m02:     Ttfb Avg:                   0.621
smc73-m02:     Ttfb Min:                   0.089
smc73-m02:     Duration 90th-ile:          1.076
smc73-m02:     Duration 99th-ile:          1.600
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         95.654
smc73-m02:     Total Transferred (MB):     829440.000
smc73-m02:     Ttfb 90th-ile:              0.974
smc73-m02:     Ttfb 99th-ile:              1.409
```

## 16.9. 512 sessions

```
workload 16
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 10240
smc73-m02:     objectSize (MB):            16.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1553.249
smc73-m02:     Duration Max:               20.971
smc73-m02:     Duration Avg:               5.169
smc73-m02:     Duration Min:               0.721
smc73-m02:     Ttfb Max:                   20.971
smc73-m02:     Ttfb Avg:                   5.169
smc73-m02:     Ttfb Min:                   0.721
smc73-m02:     Duration 90th-ile:          10.487
smc73-m02:     Duration 99th-ile:          15.472
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         105.482
smc73-m02:     Total Transferred (MB):     163840.000
smc73-m02:     Ttfb 90th-ile:              10.487
smc73-m02:     Ttfb 99th-ile:              15.472
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       51200
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    8604.463
smc73-m02:     Duration Max:               2.763
smc73-m02:     Duration Avg:               0.942
smc73-m02:     Duration Min:               0.199
smc73-m02:     Ttfb Max:                   2.718
smc73-m02:     Ttfb Avg:                   0.896
smc73-m02:     Ttfb Min:                   0.189
smc73-m02:     Duration 90th-ile:          1.305
smc73-m02:     Duration 99th-ile:          1.699
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         95.206
smc73-m02:     Total Transferred (MB):     819200.000
smc73-m02:     Ttfb 90th-ile:              1.254
smc73-m02:     Ttfb 99th-ile:              1.634
```


# 17. TTFB, 64 MB, 1-512 sessions

## 17.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 1
  batch_id: ttfb-v03-64Mb
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n    32 -c   1 -o 64Mb -e 3 -- -sampleReads 10
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   448 -c  16 -o 64Mb -e 3 -- -sampleReads 10
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   896 -c  32 -o 64Mb -e 3 -- -sampleReads 10
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c  64 -o 64Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c 128 -o 64Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c 256 -o 64Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5376 -c 384 -o 64Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  5120 -c 512 -o 64Mb -e 3 -- -sampleReads  5

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 17.2. 1 session

```

workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 32
smc73-m02:     objectSize (MB):            64.000
smc73-m02:     sampleReads:                10
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       32
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    23.832
smc73-m02:     Duration Max:               3.230
smc73-m02:     Duration Avg:               2.685
smc73-m02:     Duration Min:               2.443
smc73-m02:     Ttfb Max:                   3.230
smc73-m02:     Ttfb Avg:                   2.685
smc73-m02:     Ttfb Min:                   2.443
smc73-m02:     Duration 90th-ile:          3.176
smc73-m02:     Duration 99th-ile:          3.230
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         85.934
smc73-m02:     Total Transferred (MB):     2048.000
smc73-m02:     Ttfb 90th-ile:              3.176
smc73-m02:     Ttfb 99th-ile:              3.230
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       320
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    497.331
smc73-m02:     Duration Max:               0.473
smc73-m02:     Duration Avg:               0.129
smc73-m02:     Duration Min:               0.115
smc73-m02:     Ttfb Max:                   0.421
smc73-m02:     Ttfb Avg:                   0.074
smc73-m02:     Ttfb Min:                   0.063
smc73-m02:     Duration 90th-ile:          0.139
smc73-m02:     Duration 99th-ile:          0.181
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         41.180
smc73-m02:     Total Transferred (MB):     20480.000
smc73-m02:     Ttfb 90th-ile:              0.077
smc73-m02:     Ttfb 99th-ile:              0.118
```

## 17.3. 16 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 448
smc73-m02:     objectSize (MB):            64.000
smc73-m02:     sampleReads:                10
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       448
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    424.507
smc73-m02:     Duration Max:               3.843
smc73-m02:     Duration Avg:               2.376
smc73-m02:     Duration Min:               1.535
smc73-m02:     Ttfb Max:                   3.843
smc73-m02:     Ttfb Avg:                   2.376
smc73-m02:     Ttfb Min:                   1.535
smc73-m02:     Duration 90th-ile:          2.786
smc73-m02:     Duration 99th-ile:          3.237
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         67.542
smc73-m02:     Total Transferred (MB):     28672.000
smc73-m02:     Ttfb 90th-ile:              2.786
smc73-m02:     Ttfb 99th-ile:              3.237
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       4480
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3751.115
smc73-m02:     Duration Max:               1.642
smc73-m02:     Duration Avg:               0.273
smc73-m02:     Duration Min:               0.129
smc73-m02:     Ttfb Max:                   0.730
smc73-m02:     Ttfb Avg:                   0.143
smc73-m02:     Ttfb Min:                   0.068
smc73-m02:     Duration 90th-ile:          0.343
smc73-m02:     Duration 99th-ile:          0.646
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         76.436
smc73-m02:     Total Transferred (MB):     286720.000
smc73-m02:     Ttfb 90th-ile:              0.188
smc73-m02:     Ttfb 99th-ile:              0.352
```

## 17.4. 32 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 896
smc73-m02:     objectSize (MB):            64.000
smc73-m02:     sampleReads:                10
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       896
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    869.394
smc73-m02:     Duration Max:               3.272
smc73-m02:     Duration Avg:               2.307
smc73-m02:     Duration Min:               1.640
smc73-m02:     Ttfb Max:                   3.272
smc73-m02:     Ttfb Avg:                   2.307
smc73-m02:     Ttfb Min:                   1.640
smc73-m02:     Duration 90th-ile:          2.626
smc73-m02:     Duration 99th-ile:          3.006
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         65.959
smc73-m02:     Total Transferred (MB):     57344.000
smc73-m02:     Ttfb 90th-ile:              2.626
smc73-m02:     Ttfb 99th-ile:              3.006
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       8960
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    4954.582
smc73-m02:     Duration Max:               1.768
smc73-m02:     Duration Avg:               0.413
smc73-m02:     Duration Min:               0.138
smc73-m02:     Ttfb Max:                   1.547
smc73-m02:     Ttfb Avg:                   0.187
smc73-m02:     Ttfb Min:                   0.075
smc73-m02:     Duration 90th-ile:          0.516
smc73-m02:     Duration 99th-ile:          0.783
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         115.739
smc73-m02:     Total Transferred (MB):     573440.000
smc73-m02:     Ttfb 90th-ile:              0.256
smc73-m02:     Ttfb 99th-ile:              0.493
```

## 17.5. 64 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            64.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1668.001
smc73-m02:     Duration Max:               8.603
smc73-m02:     Duration Avg:               2.440
smc73-m02:     Duration Min:               1.279
smc73-m02:     Ttfb Max:                   8.603
smc73-m02:     Ttfb Avg:                   2.440
smc73-m02:     Ttfb Min:                   1.279
smc73-m02:     Duration 90th-ile:          4.717
smc73-m02:     Duration 99th-ile:          7.453
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         196.451
smc73-m02:     Total Transferred (MB):     327680.000
smc73-m02:     Ttfb 90th-ile:              4.717
smc73-m02:     Ttfb 99th-ile:              7.453
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       25600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5910.209
smc73-m02:     Duration Max:               1.877
smc73-m02:     Duration Avg:               0.693
smc73-m02:     Duration Min:               0.145
smc73-m02:     Ttfb Max:                   1.446
smc73-m02:     Ttfb Avg:                   0.211
smc73-m02:     Ttfb Min:                   0.078
smc73-m02:     Duration 90th-ile:          0.886
smc73-m02:     Duration 99th-ile:          1.226
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         277.215
smc73-m02:     Total Transferred (MB):     1638400.000
smc73-m02:     Ttfb 90th-ile:              0.298
smc73-m02:     Ttfb 99th-ile:              0.620
```

## 17.6. 128 sessions

```
workload 10
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            64.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1406.779
smc73-m02:     Duration Max:               17.275
smc73-m02:     Duration Avg:               5.768
smc73-m02:     Duration Min:               1.410
smc73-m02:     Ttfb Max:                   17.275
smc73-m02:     Ttfb Avg:                   5.768
smc73-m02:     Ttfb Min:                   1.410
smc73-m02:     Duration 90th-ile:          9.396
smc73-m02:     Duration 99th-ile:          13.042
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         232.929
smc73-m02:     Total Transferred (MB):     327680.000
smc73-m02:     Ttfb 90th-ile:              9.396
smc73-m02:     Ttfb 99th-ile:              13.042
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       25600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    7052.337
smc73-m02:     Duration Max:               3.031
smc73-m02:     Duration Avg:               1.160
smc73-m02:     Duration Min:               0.165
smc73-m02:     Ttfb Max:                   1.640
smc73-m02:     Ttfb Avg:                   0.367
smc73-m02:     Ttfb Min:                   0.081
smc73-m02:     Duration 90th-ile:          1.773
smc73-m02:     Duration 99th-ile:          2.245
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         232.320
smc73-m02:     Total Transferred (MB):     1638400.000
smc73-m02:     Ttfb 90th-ile:              0.600
smc73-m02:     Ttfb 99th-ile:              1.051
```

## 17.7. 256 sessions

```
workload 12
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            64.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1415.287
smc73-m02:     Duration Max:               22.756
smc73-m02:     Duration Avg:               11.355
smc73-m02:     Duration Min:               1.592
smc73-m02:     Ttfb Max:                   22.756
smc73-m02:     Ttfb Avg:                   11.355
smc73-m02:     Ttfb Min:                   1.592
smc73-m02:     Duration 90th-ile:          16.479
smc73-m02:     Duration 99th-ile:          18.729
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         231.529
smc73-m02:     Total Transferred (MB):     327680.000
smc73-m02:     Ttfb 90th-ile:              16.479
smc73-m02:     Ttfb 99th-ile:              18.729
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       25600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    7290.523
smc73-m02:     Duration Max:               6.706
smc73-m02:     Duration Avg:               2.239
smc73-m02:     Duration Min:               0.185
smc73-m02:     Ttfb Max:                   3.405
smc73-m02:     Ttfb Avg:                   0.660
smc73-m02:     Ttfb Min:                   0.082
smc73-m02:     Duration 90th-ile:          3.482
smc73-m02:     Duration 99th-ile:          4.090
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         224.730
smc73-m02:     Total Transferred (MB):     1638400.000
smc73-m02:     Ttfb 90th-ile:              1.270
smc73-m02:     Ttfb 99th-ile:              1.956
```

## 17.8. 384 sessions

```
workload 14
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 5376
smc73-m02:     objectSize (MB):            64.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5376
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    2141.792
smc73-m02:     Duration Max:               30.449
smc73-m02:     Duration Avg:               11.108
smc73-m02:     Duration Min:               1.852
smc73-m02:     Ttfb Max:                   30.449
smc73-m02:     Ttfb Avg:                   11.108
smc73-m02:     Ttfb Min:                   1.852
smc73-m02:     Duration 90th-ile:          17.544
smc73-m02:     Duration 99th-ile:          22.951
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         160.643
smc73-m02:     Total Transferred (MB):     344064.000
smc73-m02:     Ttfb 90th-ile:              17.544
smc73-m02:     Ttfb 99th-ile:              22.951
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       26880
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5600.644
smc73-m02:     Duration Max:               11.735
smc73-m02:     Duration Avg:               4.351
smc73-m02:     Duration Min:               0.506
smc73-m02:     Ttfb Max:                   7.587
smc73-m02:     Ttfb Avg:                   2.286
smc73-m02:     Ttfb Min:                   0.090
smc73-m02:     Duration 90th-ile:          6.598
smc73-m02:     Duration 99th-ile:          8.365
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         307.165
smc73-m02:     Total Transferred (MB):     1720320.000
smc73-m02:     Ttfb 90th-ile:              3.861
smc73-m02:     Ttfb 99th-ile:              5.183
```

## 17.9. 512 sessions

```
workload 16
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 5120
smc73-m02:     objectSize (MB):            64.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1925.243
smc73-m02:     Duration Max:               42.800
smc73-m02:     Duration Avg:               16.447
smc73-m02:     Duration Min:               2.106
smc73-m02:     Ttfb Max:                   42.800
smc73-m02:     Ttfb Avg:                   16.447
smc73-m02:     Ttfb Min:                   2.106
smc73-m02:     Duration 90th-ile:          24.687
smc73-m02:     Duration 99th-ile:          30.114
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         170.202
smc73-m02:     Total Transferred (MB):     327680.000
smc73-m02:     Ttfb 90th-ile:              24.687
smc73-m02:     Ttfb 99th-ile:              30.114
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       25600
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5075.489
smc73-m02:     Duration Max:               18.950
smc73-m02:     Duration Avg:               6.395
smc73-m02:     Duration Min:               0.401
smc73-m02:     Ttfb Max:                   13.025
smc73-m02:     Ttfb Avg:                   3.305
smc73-m02:     Ttfb Min:                   0.149
smc73-m02:     Duration 90th-ile:          9.553
smc73-m02:     Duration 99th-ile:          12.739
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         322.806
smc73-m02:     Total Transferred (MB):     1638400.000
smc73-m02:     Ttfb 90th-ile:              5.470
smc73-m02:     Ttfb 99th-ile:              7.494
```

# 18. TTFB, 128 MB, 1-512 sessions

## 18.1. PerfLine job YAML

```yaml
common:
  version: 1
  description: EOS-16575 - initial R2 perf test
  priority: 1
  batch_id: ttfb-v03-128Mb
  user: ivan.tishchenko@seagate.com
  send_email: false

workload:
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n 64 -c 64 -o 256Mb -e 3
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n    16 -c   1 -o 128Mb -e 3 -- -sampleReads 40
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   224 -c  16 -o 128Mb -e 3 -- -sampleReads 10
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n   448 -c  32 -o 128Mb -e 3 -- -sampleReads 10
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  1024 -c  64 -o 128Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2048 -c 128 -o 128Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2048 -c 256 -o 128Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2304 -c 384 -o 128Mb -e 3 -- -sampleReads  5
  - cmd: sleep 15
  - cmd: /root/perfline/perfline/workload/s3bench_remote.sh -n  2048 -c 512 -o 128Mb -e 3 -- -sampleReads  5

execution_options:
  mkfs: false
  no_m0trace_files: true
  no_m0trace_dumps: true
  no_addb_stobs: true
  no_addb_dumps: true
  no_m0play_db: true
```

## 18.2. 1 session

```
workload 2
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 1
smc73-m02:     numSamples:                 16
smc73-m02:     objectSize (MB):            128.000
smc73-m02:     sampleReads:                40
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       16
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    29.665
smc73-m02:     Duration Max:               5.458
smc73-m02:     Duration Avg:               4.315
smc73-m02:     Duration Min:               3.722
smc73-m02:     Ttfb Max:                   5.458
smc73-m02:     Ttfb Avg:                   4.315
smc73-m02:     Ttfb Min:                   3.722
smc73-m02:     Duration 90th-ile:          4.679
smc73-m02:     Duration 99th-ile:          5.458
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         69.037
smc73-m02:     Total Transferred (MB):     2048.000
smc73-m02:     Ttfb 90th-ile:              4.679
smc73-m02:     Ttfb 99th-ile:              5.458
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       640
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    523.855
smc73-m02:     Duration Max:               0.958
smc73-m02:     Duration Avg:               0.244
smc73-m02:     Duration Min:               0.205
smc73-m02:     Ttfb Max:                   0.761
smc73-m02:     Ttfb Avg:                   0.073
smc73-m02:     Ttfb Min:                   0.064
smc73-m02:     Duration 90th-ile:          0.270
smc73-m02:     Duration 99th-ile:          0.305
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         156.379
smc73-m02:     Total Transferred (MB):     81920.000
smc73-m02:     Ttfb 90th-ile:              0.078
smc73-m02:     Ttfb 99th-ile:              0.109
```

## 18.3. 16 sessions

```
workload 4
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 16
smc73-m02:     numSamples:                 224
smc73-m02:     objectSize (MB):            128.000
smc73-m02:     sampleReads:                10
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       224
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    541.701
smc73-m02:     Duration Max:               5.318
smc73-m02:     Duration Avg:               3.666
smc73-m02:     Duration Min:               2.596
smc73-m02:     Ttfb Max:                   5.318
smc73-m02:     Ttfb Avg:                   3.666
smc73-m02:     Ttfb Min:                   2.596
smc73-m02:     Duration 90th-ile:          4.021
smc73-m02:     Duration 99th-ile:          4.476
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         52.930
smc73-m02:     Total Transferred (MB):     28672.000
smc73-m02:     Ttfb 90th-ile:              4.021
smc73-m02:     Ttfb 99th-ile:              4.476
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       2240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    3997.347
smc73-m02:     Duration Max:               1.170
smc73-m02:     Duration Avg:               0.511
smc73-m02:     Duration Min:               0.250
smc73-m02:     Ttfb Max:                   0.628
smc73-m02:     Ttfb Avg:                   0.146
smc73-m02:     Ttfb Min:                   0.075
smc73-m02:     Duration 90th-ile:          0.622
smc73-m02:     Duration 99th-ile:          0.832
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         71.728
smc73-m02:     Total Transferred (MB):     286720.000
smc73-m02:     Ttfb 90th-ile:              0.189
smc73-m02:     Ttfb 99th-ile:              0.358
```

## 18.4. 32 sessions

```
workload 6
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 32
smc73-m02:     numSamples:                 448
smc73-m02:     objectSize (MB):            128.000
smc73-m02:     sampleReads:                10
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       448
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1117.642
smc73-m02:     Duration Max:               4.872
smc73-m02:     Duration Avg:               3.523
smc73-m02:     Duration Min:               2.630
smc73-m02:     Ttfb Max:                   4.872
smc73-m02:     Ttfb Avg:                   3.523
smc73-m02:     Ttfb Min:                   2.630
smc73-m02:     Duration 90th-ile:          3.958
smc73-m02:     Duration 99th-ile:          4.538
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         51.308
smc73-m02:     Total Transferred (MB):     57344.000
smc73-m02:     Ttfb 90th-ile:              3.958
smc73-m02:     Ttfb 99th-ile:              4.538
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       4480
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5410.107
smc73-m02:     Duration Max:               1.634
smc73-m02:     Duration Avg:               0.756
smc73-m02:     Duration Min:               0.264
smc73-m02:     Ttfb Max:                   0.977
smc73-m02:     Ttfb Avg:                   0.202
smc73-m02:     Ttfb Min:                   0.078
smc73-m02:     Duration 90th-ile:          0.905
smc73-m02:     Duration 99th-ile:          1.270
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         105.994
smc73-m02:     Total Transferred (MB):     573440.000
smc73-m02:     Ttfb 90th-ile:              0.266
smc73-m02:     Ttfb 99th-ile:              0.552
```

## 18.5. 64 sessions

```
workload 8
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 64
smc73-m02:     numSamples:                 1024
smc73-m02:     objectSize (MB):            128.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       1024
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    2190.051
smc73-m02:     Duration Max:               11.966
smc73-m02:     Duration Avg:               3.609
smc73-m02:     Duration Min:               2.417
smc73-m02:     Ttfb Max:                   11.966
smc73-m02:     Ttfb Avg:                   3.609
smc73-m02:     Ttfb Min:                   2.417
smc73-m02:     Duration 90th-ile:          5.757
smc73-m02:     Duration 99th-ile:          9.465
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         59.849
smc73-m02:     Total Transferred (MB):     131072.000
smc73-m02:     Ttfb 90th-ile:              5.757
smc73-m02:     Ttfb 99th-ile:              9.465
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       5120
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6577.586
smc73-m02:     Duration Max:               2.969
smc73-m02:     Duration Avg:               1.236
smc73-m02:     Duration Min:               0.280
smc73-m02:     Ttfb Max:                   1.678
smc73-m02:     Ttfb Avg:                   0.271
smc73-m02:     Ttfb Min:                   0.087
smc73-m02:     Duration 90th-ile:          1.527
smc73-m02:     Duration 99th-ile:          1.964
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         99.635
smc73-m02:     Total Transferred (MB):     655360.000
smc73-m02:     Ttfb 90th-ile:              0.366
smc73-m02:     Ttfb 99th-ile:              0.754
```

## 18.6. 128 sessions

```
workload 10
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 128
smc73-m02:     numSamples:                 2048
smc73-m02:     objectSize (MB):            128.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2048
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1617.050
smc73-m02:     Duration Max:               25.938
smc73-m02:     Duration Avg:               9.932
smc73-m02:     Duration Min:               2.685
smc73-m02:     Ttfb Max:                   25.938
smc73-m02:     Ttfb Avg:                   9.932
smc73-m02:     Ttfb Min:                   2.685
smc73-m02:     Duration 90th-ile:          17.411
smc73-m02:     Duration 99th-ile:          21.620
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         162.112
smc73-m02:     Total Transferred (MB):     262144.000
smc73-m02:     Ttfb 90th-ile:              17.411
smc73-m02:     Ttfb 99th-ile:              21.620
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5779.256
smc73-m02:     Duration Max:               8.017
smc73-m02:     Duration Avg:               2.826
smc73-m02:     Duration Min:               0.324
smc73-m02:     Ttfb Max:                   2.495
smc73-m02:     Ttfb Avg:                   0.382
smc73-m02:     Ttfb Min:                   0.108
smc73-m02:     Duration 90th-ile:          3.731
smc73-m02:     Duration 99th-ile:          4.948
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         226.797
smc73-m02:     Total Transferred (MB):     1310720.000
smc73-m02:     Ttfb 90th-ile:              0.649
smc73-m02:     Ttfb 99th-ile:              1.770
```

## 18.7. 256 sessions

```
workload 12
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 256
smc73-m02:     numSamples:                 2048
smc73-m02:     objectSize (MB):            128.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2048
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1536.607
smc73-m02:     Duration Max:               35.103
smc73-m02:     Duration Avg:               20.631
smc73-m02:     Duration Min:               3.794
smc73-m02:     Ttfb Max:                   35.103
smc73-m02:     Ttfb Avg:                   20.631
smc73-m02:     Ttfb Min:                   3.794
smc73-m02:     Duration 90th-ile:          26.370
smc73-m02:     Duration 99th-ile:          30.858
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         170.599
smc73-m02:     Total Transferred (MB):     262144.000
smc73-m02:     Ttfb 90th-ile:              26.370
smc73-m02:     Ttfb 99th-ile:              30.858
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    4865.917
smc73-m02:     Duration Max:               16.005
smc73-m02:     Duration Avg:               6.681
smc73-m02:     Duration Min:               0.444
smc73-m02:     Ttfb Max:                   5.263
smc73-m02:     Ttfb Avg:                   1.617
smc73-m02:     Ttfb Min:                   0.076
smc73-m02:     Duration 90th-ile:          9.470
smc73-m02:     Duration 99th-ile:          12.032
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         269.368
smc73-m02:     Total Transferred (MB):     1310720.000
smc73-m02:     Ttfb 90th-ile:              2.873
smc73-m02:     Ttfb 99th-ile:              3.958
```

## 18.8. 384 sessions

```
workload 14
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 384
smc73-m02:     numSamples:                 2304
smc73-m02:     objectSize (MB):            128.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2304
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1929.766
smc73-m02:     Duration Max:               43.555
smc73-m02:     Duration Avg:               23.867
smc73-m02:     Duration Min:               3.934
smc73-m02:     Ttfb Max:                   43.555
smc73-m02:     Ttfb Avg:                   23.867
smc73-m02:     Ttfb Min:                   3.934
smc73-m02:     Duration 90th-ile:          34.351
smc73-m02:     Duration 99th-ile:          40.680
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         152.823
smc73-m02:     Total Transferred (MB):     294912.000
smc73-m02:     Ttfb 90th-ile:              34.351
smc73-m02:     Ttfb 99th-ile:              40.680
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       11520
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    5032.056
smc73-m02:     Duration Max:               30.429
smc73-m02:     Duration Avg:               9.635
smc73-m02:     Duration Min:               0.366
smc73-m02:     Ttfb Max:                   9.360
smc73-m02:     Ttfb Avg:                   2.444
smc73-m02:     Ttfb Min:                   0.100
smc73-m02:     Duration 90th-ile:          15.274
smc73-m02:     Duration 99th-ile:          21.913
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         293.033
smc73-m02:     Total Transferred (MB):     1474560.000
smc73-m02:     Ttfb 90th-ile:              5.405
smc73-m02:     Ttfb 99th-ile:              7.417
```

## 18.9. 512 sessions

```
workload 16
3
smc73-m02:  Version:                    2020-04-08-07:38:44-4f7d65ecd3aaa644c4d2304c6818711c2d2cfdda
smc73-m02:  Parameters:
smc73-m02:     numClients:                 512
smc73-m02:     numSamples:                 2048
smc73-m02:     objectSize (MB):            128.000
smc73-m02:     sampleReads:                5
smc73-m02:     clientDelay:                1
smc73-m02:     readObj:                    true
smc73-m02:     headObj:                    false
smc73-m02:     putObjTag:                  false
smc73-m02:     getObjTag:                  false
smc73-m02:     bucket:                     bmax
smc73-m02:     deleteAtOnce:               1000
smc73-m02:     endpoints:
smc73-m02:        http://192.168.48.155
smc73-m02:        http://192.168.48.157
smc73-m02:        http://192.168.48.159
smc73-m02:     jsonOutput:                 false
smc73-m02:     numTags:                    10
smc73-m02:     objectNamePrefix:           loadgen_test_
smc73-m02:     reportFormat:               Version;Parameters;Parameters:numClients;Parameters:numSamples;Parameters:objectSize (MB);Parameters:sampleReads;Parameters:clientDelay;Parameters:readObj;Parameters:headObj;Parameters:putObjTag;Parameters:getObjTag;Tests:Operation;Tests:Total Requests Count;Tests:Errors Count;Tests:Total Throughput (MB/s);Tests:Duration Max;Tests:Duration Avg;Tests:Duration Min;Tests:Ttfb Max;Tests:Ttfb Avg;Tests:Ttfb Min;-Tests:Duration 25th-ile;-Tests:Duration 50th-ile;-Tests:Duration 75th-ile;-Tests:Ttfb 25th-ile;-Tests:Ttfb 50th-ile;-Tests:Ttfb 75th-ile;
smc73-m02:     tagNamePrefix:              tag_name_
smc73-m02:     tagValPrefix:               tag_val_
smc73-m02:     verbose:                    false
smc73-m02:  Tests:
smc73-m02:     Operation:                  Write
smc73-m02:     Total Requests Count:       2048
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    1802.451
smc73-m02:     Duration Max:               55.846
smc73-m02:     Duration Avg:               33.301
smc73-m02:     Duration Min:               6.383
smc73-m02:     Ttfb Max:                   55.846
smc73-m02:     Ttfb Avg:                   33.301
smc73-m02:     Ttfb Min:                   6.383
smc73-m02:     Duration 90th-ile:          42.801
smc73-m02:     Duration 99th-ile:          51.525
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         145.437
smc73-m02:     Total Transferred (MB):     262144.000
smc73-m02:     Ttfb 90th-ile:              42.801
smc73-m02:     Ttfb 99th-ile:              51.525
smc73-m02:
smc73-m02:     Operation:                  Read
smc73-m02:     Total Requests Count:       10240
smc73-m02:     Errors Count:               0
smc73-m02:     Total Throughput (MB/s):    6069.223
smc73-m02:     Duration Max:               22.988
smc73-m02:     Duration Avg:               10.664
smc73-m02:     Duration Min:               0.334
smc73-m02:     Ttfb Max:                   8.356
smc73-m02:     Ttfb Avg:                   2.830
smc73-m02:     Ttfb Min:                   0.077
smc73-m02:     Duration 90th-ile:          14.738
smc73-m02:     Duration 99th-ile:          18.664
smc73-m02:     Errors:                     []
smc73-m02:     Total Duration (s):         215.962
smc73-m02:     Total Transferred (MB):     1310720.000
smc73-m02:     Ttfb 90th-ile:              5.047
smc73-m02:     Ttfb 99th-ile:              6.343
```


# 19. --template-- TTFB, 1 KB, 1-512 sessions

## 19.1. PerfLine job YAML

```yaml
```

## 19.2. test 1

