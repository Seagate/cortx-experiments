# Test TTFB with Auth fixes

There is a fix, under [EOS-15268](https://jts.seagate.com/browse/EOS-15268),
which is expected to significantly improve AuthServer response time.
Which in turn improves TTFB and small object throughput

Contents:

-   [Test TTFB with Auth fixes](#test-ttfb-with-auth-fixes)

    -   [Corresponding Jira Ticket](#corresponding-jira-ticket)

    -   [Objectives](#objectives)

    -   [Initial Tests](#initial-tests)

        -   [Branches and repos](#branches-and-repos)
        -   [Workloads](#workloads)
        -   [Results](#results)

    -   [POC Details](#poc-details)

    -   [Results](#results)

    -   [Analysis](#analysis)

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

### Results

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

Addb analysis is required since it is unclear for the moment why there are no
expected improvements that were observed in tests on VM.
