Running Auth call in parallel with Motr KVS call
================================================

Most of the S3 API calls invoke two calls between s3server and s3authserver:

1 Authentication
1 Authorization

These calls are intermixed with Motr KVS calls, and are done sequentially one after another.
It should be possible to run these calls, or one of them, in parallel.
This would improve TTFB and small objects performance.


Contents:

- [Running Auth call in parallel with Motr KVS call](#running-auth-call-in-parallel-with-motr-kvs-call)
- [Corresponding Jira Ticket](#corresponding-jira-ticket)
- [Objectives](#objectives)
- [POC Details](#poc-details)
- [Results](#results)
- [Analysis](#analysis)
  - [Intro](#intro)
  - [Normal configuration](#normal-configuration)
  - [All auth calls are parallel to request execution](#all-auth-calls-are-parallel-to-request-execution)
  - [Only one auth call is done in parallel while the other is sequential](#only-one-auth-call-is-done-in-parallel-while-the-other-is-sequential)


Corresponding Jira Ticket
=========================

[EOS-16658](https://jts.seagate.com/browse/EOS-16658)


Objectives
==========

Identify if it is possible to run both auth calls, or some of them, in parallel
with KVS ops and request processing.

Measure or estimate the impact the parallel auth execution could have on
performance metrics.


POC Details
===========

Both auth calls are independent. Authentication requires only request data and
authorization requires metadata from the motr kvs. Request execution doesn't
depend on any data from auth server. It looks like nothing prevents auth to work
in parallel to request processing.

It is required to test following combinations:

* All auth calls are parallel to request execution
  The happy path for full auth in parallel configuration could easily be emulated
  by disabling auth at all. S3server has a special option to do this - **disable_auth**.

* Only one auth call is done in parallel while the other is sequential
  Such a configuration couldn't be easily implemented, but it could be estimated.
  To do this normal configuration is run and addb metrics are collected. Based on
  addb all auth calls are measured. Required auth configuration impact
  could be estimated by substructing call duration from total request time.


Results
=======

All tests were run with objects of size 4KB and different number of clients per cluster - 250, 500 and 750.
During each run all types of object and metadata requests were measured.

* Normal configuration

| number of clients    | 250        |           |           |         |         | 500     |           |           |         |        | 750     |           |           |          |          |
| -------------------- | ---------- | --------- | --------- | ------- | ------- | ------- | --------- | --------- | ------- | ------ | ------- | --------- | --------- | -------- | -------- |
|                      | Write      | PutObjTag | GetObjTag | HeadObj | Read    | Write   | PutObjTag | GetObjTag | HeadObj | Read   | Write   | PutObjTag | GetObjTag | HeadObj  | Read     |
| RPS                  | 29.656     | 322.670   | 726.203   | 772.106 | 700.974 | 159.711 | 343.015   | 590.023   | 594.26  | 576.05 | 179.187 | 313.731   | 439.693   | 502.868  | 466.460  |
| Total Requests Count | 232        | 232       | 232000    | 232000  | 232000  | 500     | 500       | 500000    | 500000  | 500000 | 750     | 750       | 750000    | 749939   | 749875   |
| Errors Count         | 18         | 18        | 18000     | 18000   | 18000   | 0       | 0         | 0         | 0       | 0      | 0       | 0         | 0         | 61       | 125      |
| Total Duration (s)   | 7.823      | 0.719     | 319.47    | 300.477 | 330.968 | 3.131   | 1.458     | 847.425   | 841.383 | 867.98 | 4.186   | 2.391     | 1705.734  | 1491.325 | 1607.588 |
| Duration Max         | 7.813      | 0.719     | 1.846     | 1.708   | 1.834   | 3.1     | 1.451     | 2.408     | 2.712   | 2.713  | 4.164   | 2.375     | 3.716     | 30.188   | 30.664   |
| Duration Avg         | 3.9        | 0.532     | 0.319     | 0.301   | 0.332   | 1.971   | 1.027     | 0.847     | 0.841   | 0.868  | 2.936   | 1.551     | 1.705     | 1.477    | 1.598    |
| Duration Min         | 1.581      | 0.273     | 0.007     | 0.023   | 0.014   | 1.209   | 0.282     | 0.017     | 0.012   | 0.028  | 1.632   | 0.252     | 0.015     | 0.013    | 0.024    |
| Ttfb Max             | 7.813      | 0.719     | 1.846     | 1.708   | 1.834   | 3.1     | 1.451     | 2.408     | 2.712   | 2.713  | 4.164   | 2.375     | 3.716     | 30.188   | 30.664   |
| Ttfb Avg             | 3.9        | 0.532     | 0.319     | 0.301   | 0.331   | 1.971   | 1.027     | 0.847     | 0.841   | 0.868  | 2.936   | 1.551     | 1.705     | 1.477    | 1.598    |
| Ttfb Min             | 1.581      | 0.273     | 0.007     | 0.023   | 0.014   | 1.209   | 0.282     | 0.017     | 0.012   | 0.028  | 1.632   | 0.252     | 0.015     | 0.013    | 0.024    |
| Duration 90th-ile    | 6.905      | 0.676     | 0.476     | 0.361   | 0.397   | 2.493   | 1.352     | 0.939     | 0.933   | 0.968  | 3.828   | 2.033     | 1.83      | 1.747    | 1.621    |
| Duration 99th-ile    | 7.811      | 0.716     | 0.929     | 0.733   | 0.856   | 3.079   | 1.446     | 1.404     | 1.333   | 1.393  | 4.153   | 2.348     | 2.267     | 7.147    | 7.422    |
| Ttfb 90th-ile        | 6.905      | 0.676     | 0.476     | 0.361   | 0.397   | 2.493   | 1.352     | 0.939     | 0.933   | 0.968  | 3.828   | 2.033     | 1.83      | 1.747    | 1.621    |
| Ttfb 99th-ile        | 7.811      | 0.716     | 0.929     | 0.733   | 0.856   | 3.079   | 1.446     | 1.404     | 1.333   | 1.393  | 4.153   | 2.348     | 2.267     | 7.147    | 7.422    |

* Auth call durations based on addb - [hist_auth.png](hist_auth.png)

| phase       | min, s  | avg, s  | max, s  |
| ----------- | ------- | ------- | ------- |
| check_auth  | 0.00103 | 0.13648 | 3.78818 |
| check_authz | 0.00066 | 0.01167 | 3.26455 |

* All auth calls are parallel to request execution

| number of clients    | 250     |           |           |          |          | 500     |           |           |          |          | 750     |           |           |         |        |
| -------------------- | ------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | ------- | ------ |
|                      | Write   | PutObjTag | GetObjTag | HeadObj  | Read     | Write   | PutObjTag | GetObjTag | HeadObj  | Read     | Write   | PutObjTag | GetObjTag | HeadObj | Read   |
| RPS                  | 100.806 | 364.463   | 1124.704  | 1334.132 | 1167.123 | 209.125 | 751.653   | 1141.498  | 1125.148 | 1041.288 | 195.727 | 744.877   | 946.838   | 950.071 | 915.08 |
| Total Requests Count | 250     | 250       | 250000    | 250000   | 250000   | 500     | 500       | 500000    | 500000   | 500000   | 750     | 750       | 750000    | 750000  | 750000 |
| Errors Count         | 0       | 0         | 0         | 0        | 0        | 0       | 0         | 0         | 0        | 0        | 0       | 0         | 0         | 0       | 0      |
| Total Duration (s)   | 2.48    | 0.686     | 222.281   | 187.388  | 214.202  | 2.391   | 0.665     | 438.021   | 444.386  | 480.175  | 3.832   | 1.007     | 792.11    | 789.415 | 819.6  |
| Duration Max         | 2.47    | 0.684     | 3.446     | 3.06     | 3.011    | 2.368   | 0.661     | 2.092     | 2.429    | 3.544    | 3.826   | 0.993     | 3.465     | 2.917   | 5.232  |
| Duration Avg         | 1.534   | 0.446     | 0.222     | 0.187    | 0.214    | 1.382   | 0.489     | 0.438     | 0.444    | 0.48     | 2.148   | 0.608     | 0.792     | 0.789   | 0.819  |
| Duration Min         | 1.089   | 0.28      | 0.009     | 0.005    | 0.008    | 0.905   | 0.022     | 0.015     | 0.01     | 0.01     | 1.052   | 0.248     | 0.012     | 0.014   | 0.012  |
| Ttfb Max             | 2.47    | 0.684     | 3.446     | 3.06     | 3.011    | 2.368   | 0.661     | 2.092     | 2.429    | 3.544    | 3.826   | 0.993     | 3.465     | 2.917   | 5.232  |
| Ttfb Avg             | 1.534   | 0.446     | 0.222     | 0.187    | 0.214    | 1.382   | 0.489     | 0.438     | 0.444    | 0.48     | 2.148   | 0.608     | 0.792     | 0.789   | 0.819  |
| Ttfb Min             | 1.089   | 0.28      | 0.009     | 0.005    | 0.008    | 0.905   | 0.022     | 0.015     | 0.01     | 0.01     | 1.052   | 0.248     | 0.012     | 0.014   | 0.012  |
| Duration 90th-ile    | 1.761   | 0.639     | 0.429     | 0.198    | 0.262    | 2.056   | 0.617     | 0.536     | 0.517    | 0.661    | 2.882   | 0.909     | 0.931     | 0.945   | 1.006  |
| Duration 99th-ile    | 2.057   | 0.682     | 1.006     | 0.772    | 0.948    | 2.361   | 0.656     | 1.031     | 1.131    | 1.477    | 3.222   | 0.952     | 1.695     | 1.578   | 1.771  |
| Ttfb 90th-ile        | 1.761   | 0.639     | 0.429     | 0.198    | 0.262    | 2.056   | 0.617     | 0.536     | 0.517    | 0.661    | 2.882   | 0.909     | 0.931     | 0.945   | 1.006  |
| Ttfb 99th-ile        | 2.057   | 0.682     | 1.006     | 0.772    | 0.948    | 2.361   | 0.656     | 1.031     | 1.131    | 1.477    | 3.222   | 0.952     | 1.695     | 1.578   | 1.771  |

* Estimation for parallel authentication

| number of clients | 250    |           |           |         |         | 500     |           |           |         |         | 750     |           |           |          |          |
| ----------------- | ------ | --------- | --------- | ------- | ------- | ------- | --------- | --------- | ------- | ------- | ------- | --------- | --------- | -------- | -------- |
|                   | Write  | PutObjTag | GetObjTag | HeadObj | Read    | Write   | PutObjTag | GetObjTag | HeadObj | Read    | Write   | PutObjTag | GetObjTag | HeadObj  | Read     |
| Duration Max      | 4.0248 | 0.58252   | 1.70952   | 1.57152 | 1.69752 | 2.96352 | 1.31452   | 2.27152   | 2.57552 | 2.57652 | 0.37582 | 2.23852   | 3.57952   | 26.39982 | 26.87582 |
| Duration Avg      | 3.7635 | 0.39552   | 0.18252   | 0.16452 | 0.19552 | 1.83452 | 0.89052   | 0.71052   | 0.70452 | 0.73152 | 2.79952 | 1.41452   | 1.56852   | 1.34052  | 1.46152  |
| Duration Min      | 1.58   | 0.27197   | 0.00597   | 0.02197 | 0.01297 | 1.20797 | 0.28097   | 0.01597   | 0.01097 | 0.02697 | 1.63097 | 0.25097   | 0.01397   | 0.01197  | 0.02297  |
| Ttfb Max          | 4.0248 | 0.58252   | 1.70952   | 1.57152 | 1.69752 | 2.96352 | 1.31452   | 2.27152   | 2.57552 | 2.57652 | 0.37582 | 2.23852   | 3.57952   | 26.39982 | 26.87582 |
| Ttfb Avg          | 3.7635 | 0.39552   | 0.18252   | 0.16452 | 0.19452 | 1.83452 | 0.89052   | 0.71052   | 0.70452 | 0.73152 | 2.79952 | 1.41452   | 1.56852   | 1.34052  | 1.46152  |
| Ttfb Min          | 1.58   | 0.27197   | 0.00597   | 0.02197 | 0.01297 | 1.20797 | 0.28097   | 0.01597   | 0.01097 | 0.02697 | 1.63097 | 0.25097   | 0.01397   | 0.01197  | 0.02297  |

* Estimation for parallel authorization

| number of clients | 250    |           |           |         |         | 500     |           |           |         |         | 750     |           |           |          |          |
| ----------------- | ------ | --------- | --------- | ------- | ------- | ------- | --------- | --------- | ------- | ------- | ------- | --------- | --------- | -------- | -------- |
|                   | Write  | PutObjTag | GetObjTag | HeadObj | Read    | Write   | PutObjTag | GetObjTag | HeadObj | Read    | Write   | PutObjTag | GetObjTag | HeadObj  | Read     |
| Duration Max      | 4.5485 | 0.70733   | 1.83433   | 1.69633 | 1.82233 | 3.08833 | 1.43933   | 2.39633   | 2.70033 | 2.70133 | 0.89945 | 2.36333   | 0.45145   | 26.92345 | 27.39945 |
| Duration Avg      | 3.8883 | 0.52033   | 0.30733   | 0.28933 | 0.32033 | 1.95933 | 1.01533   | 0.83533   | 0.82933 | 0.85633 | 2.92433 | 1.53933   | 1.69333   | 1.46533  | 1.58633  |
| Duration Min      | 1.5803 | 0.27234   | 0.00634   | 0.02234 | 0.01334 | 1.20834 | 0.28134   | 0.01634   | 0.01134 | 0.02734 | 1.63134 | 0.25134   | 0.01434   | 0.01234  | 0.02334  |
| Ttfb Max          | 4.5485 | 0.70733   | 1.83433   | 1.69633 | 1.82233 | 3.08833 | 1.43933   | 2.39633   | 2.70033 | 2.70133 | 0.89945 | 2.36333   | 0.45145   | 26.92345 | 27.39945 |
| Ttfb Avg          | 3.8883 | 0.52033   | 0.30733   | 0.28933 | 0.31933 | 1.95933 | 1.01533   | 0.83533   | 0.82933 | 0.85633 | 2.92433 | 1.53933   | 1.69333   | 1.46533  | 1.58633  |
| Ttfb Min          | 1.5803 | 0.27234   | 0.00634   | 0.02234 | 0.01334 | 1.20834 | 0.28134   | 0.01634   | 0.01134 | 0.02734 | 1.63134 | 0.25134   | 0.01434   | 0.01234  | 0.02334  |

Shared [excel report](https://seagatetechnology.sharepoint.com/:x:/r/sites/gteamdrv1/tdrive1224/Performance/S3/PerfTests/POC%20Parallel%20Auth.xlsx?d=wfd664f222f124278bd8265413a1c00c2&csf=1&web=1&e=yNEJqe)


Analysis
========

Intro
-----

Full background auth execution is possible for non-modifying requests, e.g. read or
list. Requests that modify any data or metadata, e.g. put or delete, will require
authentication to be finished or object version created. However authentication
could be run in parallel with Motr KVS calls for requests of all types.

Happy path doesn't include any extra work to complete the request, but if
auth fails all the work done will be wasted.

Normal configuration
--------------------

There were two test sessions with normal configuration. Each one were run on a clean environment
after the cluster rebootstrapped. The results were rougly the same and the number of 
errors were comparable. Root cause is not clear for now.

While min duration and ttfb values are close each other for all number of clients
max values are significantly different between 250, 500 and 750 clients.

250 clients test shows the best results for duration, ttft and rps, but in the same time the
biggest number of errors. There were no errors at all in 500 clients test and there were few errors
for 750 clients tests.

Based on addb, duration of auth calls exceeds 3.5 seconds at max - huge number.

All auth calls are parallel to request execution
------------------------------------------------

These tests were the most stable, no errors at all. RPS values at least 2 times better the case with normal
auth calls for all clients. Almost the same ttfb and duration

* Normal Auth - NA
* Parallel Auth - PA

| number of clients    | 250        |           |           |          |          | 500     |           |           |          |          | 750     |           |           |          |          |
| -------------------- | ---------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | -------- | -------- |
|                      | Write      | PutObjTag | GetObjTag | HeadObj  | Read     | Write   | PutObjTag | GetObjTag | HeadObj  | Read     | Write   | PutObjTag | GetObjTag | HeadObj  | Read     |
| RPS - NA             | 29.656     | 322.670   | 726.203   | 772.106  | 700.974  | 159.711 | 343.015   | 590.023   | 594.26   | 576.05   | 179.187 | 313.731   | 439.693   | 502.868  | 466.460  |
| RPS - PA             | 100.806    | 364.463   | 1124.704  | 1334.132 | 1167.123 | 209.125 | 751.653   | 1141.498  | 1125.148 | 1041.288 | 195.727 | 744.877   | 946.838   | 950.071  | 915.08   |
| -------------------- | ---------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | -------- | -------- |
| Total Duration - NA  | 7.823      | 0.719     | 319.47    | 300.477  | 330.968  | 3.131   | 1.458     | 847.425   | 841.383  | 867.98   | 4.186   | 2.391     | 1705.734  | 1491.325 | 1607.588 |
| Total Duration - PA  | 2.48       | 0.686     | 222.281   | 187.388  | 214.202  | 2.391   | 0.665     | 438.021   | 444.386  | 480.175  | 3.832   | 1.007     | 792.11    | 789.415  | 819.6    |
| -------------------- | ---------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | -------- | -------- |
| Duration Max - NA    | 7.813      | 0.719     | 1.846     | 1.708    | 1.834    | 3.1     | 1.451     | 2.408     | 2.712    | 2.713    | 4.164   | 2.375     | 3.716     | 30.188   | 30.664   |
| Duration Avg - NA    | 3.9        | 0.532     | 0.319     | 0.301    | 0.332    | 1.971   | 1.027     | 0.847     | 0.841    | 0.868    | 2.936   | 1.551     | 1.705     | 1.477    | 1.598    |
| Duration Min - NA    | 1.581      | 0.273     | 0.007     | 0.023    | 0.014    | 1.209   | 0.282     | 0.017     | 0.012    | 0.028    | 1.632   | 0.252     | 0.015     | 0.013    | 0.024    |
| Duration Max - PA    | 2.47       | 0.684     | 3.446     | 3.06     | 3.011    | 2.368   | 0.661     | 2.092     | 2.429    | 3.544    | 3.826   | 0.993     | 3.465     | 2.917    | 5.232    |
| Duration Avg - PA    | 1.534      | 0.446     | 0.222     | 0.187    | 0.214    | 1.382   | 0.489     | 0.438     | 0.444    | 0.48     | 2.148   | 0.608     | 0.792     | 0.789    | 0.819    |
| Duration Min - PA    | 1.089      | 0.28      | 0.009     | 0.005    | 0.008    | 0.905   | 0.022     | 0.015     | 0.01     | 0.01     | 1.052   | 0.248     | 0.012     | 0.014    | 0.012    |
| -------------------- | ---------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | -------- | -------- | ------- | --------- | --------- | -------- | -------- |
| Ttfb Max - NA        | 7.813      | 0.719     | 1.846     | 1.708    | 1.834    | 3.1     | 1.451     | 2.408     | 2.712    | 2.713    | 4.164   | 2.375     | 3.716     | 30.188   | 30.664   |
| Ttfb Avg - NA        | 3.9        | 0.532     | 0.319     | 0.301    | 0.331    | 1.971   | 1.027     | 0.847     | 0.841    | 0.868    | 2.936   | 1.551     | 1.705     | 1.477    | 1.598    |
| Ttfb Min - NA        | 1.581      | 0.273     | 0.007     | 0.023    | 0.014    | 1.209   | 0.282     | 0.017     | 0.012    | 0.028    | 1.632   | 0.252     | 0.015     | 0.013    | 0.024    |
| Ttfb Max - PA        | 2.47       | 0.684     | 3.446     | 3.06     | 3.011    | 2.368   | 0.661     | 2.092     | 2.429    | 3.544    | 3.826   | 0.993     | 3.465     | 2.917    | 5.232    |
| Ttfb Avg - PA        | 1.534      | 0.446     | 0.222     | 0.187    | 0.214    | 1.382   | 0.489     | 0.438     | 0.444    | 0.48     | 2.148   | 0.608     | 0.792     | 0.789    | 0.819    |
| Ttfb Min - PA        | 1.089      | 0.28      | 0.009     | 0.005    | 0.008    | 0.905   | 0.022     | 0.015     | 0.01     | 0.01     | 1.052   | 0.248     | 0.012     | 0.014    | 0.012    |

Conclusion: Parallel execution of auth calls in happy path shows better results comparing with normal auth on small objects.
Such a difference applicable to all number of tested clients.

Only one auth call is done in parallel while the other is sequential
--------------------------------------------------------------------

Estimation shows in this case it is possible to save up to 3.7 seconds on authentication phase for all requests.
