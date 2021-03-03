# Test TTFB with Auth fixes

There is a fix, under [EOS-15268](https://jts.seagate.com/browse/EOS-15268),
which is expected to significantly improve AuthServer response time.
Which in turn improves TTFB and small object throughput

Contents:

- [Test TTFB with Auth fixes](#test-ttfb-with-auth-fixes)
  - [Corresponding Jira Ticket](#corresponding-jira-ticket)
  - [Objectives](#objectives)
  - [Initial Tests](#initial-tests)
    - [Branches and repos](#branches-and-repos)
    - [Workloads](#workloads)
    - [Report](#report)
  - [POC Details](#poc-details)
  - [Results](#results)
  - [Analysis](#analysis)
  - [Some Data](#some-data)
    - [100 bytes](#100-bytes)
    - [256 KB](#256-kb)
    - [128 MB](#128-mb)
    - [Summary](#summary)


## Corresponding Jira Ticket

[EOS-17555](https://jts.seagate.com/browse/EOS-17555)

## Objectives

Find out if latest S3 main branch is functional on R2 hardware cluster (there might
be deploy issues, as there was a recent "R1-breaking" check in related to cortx bus).

Run standard tests on the latest S3 master and compare results with the same tests on base
**R2-HW-test-base-branch** branch.

## Initial Tests

### Branches and repos

-   Hare:
    -   repo: [https://github.com/t7ko-seagate/cortx-hare](https://github.com/t7ko-seagate/cortx-hare)
    -   branch: R2-HW-test-base-branch

-   Motr:
    -   repo: [https://github.com/t7ko-seagate/cortx-motr](https://github.com/t7ko-seagate/cortx-motr)
    -   branch: R2-HW-test-base-branch

-   S3:
    -   repo: [https://github.com/t7ko-seagate/cortx-s3server](https://github.com/t7ko-seagate/cortx-s3server)
    -   branch: R2-HW-test-base-branch

### Workloads

-   256 KB throughput:
    -   [Workload-1](../initial-perf-test-on-R2/raw-test-results.md#21-perfline-job-yaml)
    -   [Workload-2](../initial-perf-test-on-R2/raw-test-results.md#31-perfline-job-yaml)

-   Tiny object TTFB:
    -   [Workload-3](../initial-perf-test-on-R2/raw-test-results.md#8-ttfb-100-bytes-1-512-sessions---take-2)

-   256 KB TTFB:
    -   [Workload-4](../initial-perf-test-on-R2/raw-test-results.md#13-ttfb-256-kb-1-512-sessions)

-   Large object TTFB:
    -   [Workload-5](../initial-perf-test-on-R2/raw-test-results.md#18-ttfb-128-mb-1-512-sessions)

### Report

[Results.csv](../initial-perf-test-on-R2/results.csv)

## POC Details

Create custom build with Hare and Motr versions as described in [Branches and Repos](#branches-and-repos)
but S3 should be built from Main branch.

Deploy custom build to the same R2 cluster and run [Workloads](#workloads).

Take notes about all the issues faced during the deployment and run.

Results should be compared with [Results.csv](../initial-perf-test-on-R2/results.csv)

## Results

Custom build were made with help of [Jenkins CI pipeline for custom build](http://eos-jenkins.colo.seagate.com/job/GitHub-custom-ci-builds/job/centos-7.8/job/cortx-custom-ci/).

Deployment process were simple and straightforward. No issues were found.

Small and tiny objects tests were run smoothly. However there were errors
during large objects testing. Most likely those errors were caused by AuthServer.
All tests were run again after the AuthServer was restarted.

Results could be find in [Results.csv](results.csv)

## Analysis

S3server can be deployed and tested on R2 hardware after the R1-breaking changes.

Results comparison report is shared as [Excel Report](https://seagatetechnology.sharepoint.com/:x:/r/sites/gteamdrv1/tdrive1224/Performance/S3/PerfTests/Branch%20Main%20vs%20R2-hw-base-test%20-%20Copy.xlsx?d=wc0bfbf1a618543f98d199f7b74873ed1&csf=1&web=1&e=AjvtEu)

The **State** column identifies results

-   `initial` - results of the base build tests
-   `fix` - first test session with errors before AuthServer restart
-   `restart` - repeated tests after AuthServer restart
-   `restart-2` - additional tests run after one more AuthServer restart

Unclear behavior of AuthServer was reproduced in base build as well, so it is
unlikely it was caused by the tested AuthServer changes. Tests runs containing
errors - marked as `fix` - should be excluded from the comparison. Tests sessions
marked as `restart` and `restart-2` have better numbers that `fix`.

However expected TTFB and Duration improvements were not reached with the
tested AuthServer fix as expected. In some case small degradation is observed.

ADDB analysis is required since it is unclear for the moment why there are no
expected improvements that were observed in tests on VM.


## Some Data

By Ivan Tishchenko.

I was specifically looking at Reads, because we expect improvement in TTFB, and
writes operation does not have such metric by definition.

From Dmitry CSV, I took only 'initial' and 'restart'.  Ignored 'fix', because it
had some configuration issue and lots of IOs failed.  ('restart' fixed that
config issue and is more "clean" for comparison.)  I also ignored object size
256 MB, since that was "warm-up" workload, not intended for analysis and
comparison.

After that I got test results for 3 object sizes: tiny (100 bytes), small (256
KB) and large (128 MB).  Results:


### 100 bytes

| `numClients` | `ttfb_avg_init` | `ttfb_avg_restart` |  `improved` | `degraded`  | 
| ---------- | ------------- | ---------------- | -------- | -------- |
| 1          | 0.014         | 0.013            | 11%      |          |
| 16         | 0.036         | 0.024            | 33%      |          |
| 32         | 0.041         | 0.049            |          | -19%     |
| 64         | 0.053         | 0.068            |          | -28%     |
| 128        | 0.089         | 0.139            |          | -56%     |
| 256        | 0.169         | 0.241            |          | -43%     |
| 384        | 0.360         | 0.405            |          | -13%     |
| 512        | 0.743         | 0.596            | 20%      |          |

Table shows average TTFB for `init` (baseline version of s3) and `restart`
(latest main with corrected environment).

We can see that there is an improvement for 1, 16, and 512 sessions, and
degradation for the rest of experiments in the middle.

### 256 KB

| `numClients` | `init_1` | `init_2` | `restart_1` | `restart_2` | `improved` | `degraded`   |
| ------------ | -------- | -------- | ----------- | ----------- | ---------- | ------------ |
| 1            | 0.015    |          | 0.015       |             |            | -1%          |
| 16           | 0.026    |          | 0.024       |             | 9%         |              |
| 32           | 0.035    | 0.036    | 0.024       | 0.032       | 10% to 32% |              |
| 64           | 0.045    | 0.047    | 0.036       | 0.048       | +24%       | -7%          |
| 80           | 0.048    |          | 0.054       |             |            | -13%         |
| 100          | 0.069    |          | 0.098       |             |            | -43%         |
| 128          | 0.071    | 0.078    | 0.117       | 0.122       |            | -50% to -73% |
| 256          | 0.249    | 0.14 (*) | 0.229       | 0.230       | 8%         |              |
| 384          | 0.315    | 0.378    | 0.401       | 0.490       |            | -6% to -56%  |
| 512          | 0.624    | 0.528    | 0.536       | 0.625       | 14%        | -18%         |

(*) This sample seems too much inconsistent, probably measurement error.

For some of clients, test was run twice, so there are two columns for `init`
version, and two columns for `restart` version.  All these show average TTFB.
It can be seen that TTFB change is not consistent -- in some tests it shows
improvement, in some others -- degradation, with no visible pattern.


### 128 MB

| `numClients` | `ttfb_avg_init` | `ttfb_avg_restart` | `improved` | `degraded` |
| ------------ | --------------- | ------------------ | ---------- | ---------- |
| 1            | 0.073           | 0.086              |            | -17%       |
| 16           | 0.146           | 0.136              | 7%         |            |
| 32           | 0.202           | 0.155              | 23%        |            |
| 64           | 0.271           | 0.154              | 43%        |            |
| 128          | 0.382           | 0.180              | 53%        |            |
| 256          | 1.617           | 0.528              | 67%        |            |
| 384          | 2.444           | 1.063              | 57%        |            |
| 512          | 2.83            | 3.417              |            | -21%       |

Surprisingly, 128 MB shows good improvement in TTFB (except 1 and 512 sessions).
Surprise is -- the improvement is too big.  We only expected minor improvement
(because auth is relatively short as compared to data transfers).


### Summary

* We confirmed that latest S3 server code from `main` branch is working on 3
  node R2 HW setup -- POSITIVE.
* Measurement results are chaotic and not consistent.  This seems to indicate
  that either HW was not stable, or test is not stable (e.g. too short), or --
  the fixes between `init` and `restart` versions brought in some significant
  instability into TTFB -- UNDEFINED.

Conclusion: need further testing.