
Adding In-Memory Cache For Bucket Metadata
==========================================

Contents

- [Adding In-Memory Cache For Bucket Metadata](#adding-in-memory-cache-for-bucket-metadata)
- [Goal of the POC](#goal-of-the-poc)
- [Essence of the proposed change](#essence-of-the-proposed-change)
  - [Q: Main downside](#q-main-downside)
  - [But.... we will lose consistency during transition time?](#but-we-will-lose-consistency-during-transition-time)
- [Steps of the POC](#steps-of-the-poc)
  - [1- Identify how much improvement we get](#1--identify-how-much-improvement-we-get)
  - [2- Review code and see what other trade offs we'll need](#2--review-code-and-see-what-other-trade-offs-well-need)
- [POC Results](#poc-results)
  - [1- Performance test](#1--performance-test)
  - [2- Feasibility study](#2--feasibility-study)


Goal of the POC
===============

Confirm that proposed caching mechanism:

* Will improve performance.
* Is feasible.


Essence of the proposed change
==============================

In earlier experiments, it was discovered, that big part of time spent at the
beginning of each operation (e.g. PUT Object or GET Object) is spent on loading
metadata (bucket metadata and object metadata).  Metadata is loaded from Motr
KVS, and it might get slow under load.

Proposal: instead of loading bucket MD on every PUT/GET operation, load it once
and cache it in-memory.  Then access time will be taking near-zero time.

Q: Main downside
----------------

* There is no way to force-invalidate the cache in case there is metadata change
  (e.g. tags added to Bucket, or ACLs are added/modified).

Work-around:

* Implement expiration time on cache entries (e.g. entry is only valid for `N`
  seconds, after that it is discarded and reloaded).

But.... we will lose consistency during transition time?
----------------------

* User modifies the metadata, but old version of it is still cached in memory in
  other S3 instances.

Work-around:

* If there is an API call which modifies bucket metadata, S3 server will update
  metadata, then API call will be put on hold for `N` seconds (`N` is the same
  as configured above), and only then return `Success` to the caller.
  
  This will not resolve inconsistency completely, but will at least help the
  caller to know when the change is fully propagated throughout the cluster.


Steps of the POC
================

1- Identify how much improvement we get
--------------------------------

Take the very basic cache implementation, and run comparative test:

* With original code (which does KVS fetch on every PUT/GET), versus
* Modified code (which loads it once then does in-memory cache lookup).

See what is the improvement.


2- Review code and see what other trade offs we'll need
-------------------------------------------------------

Are there any other corner cases similar to consistency issue listed above?


POC Results
===========

1- Performance test
--------------------

See [full s3bench output](2020.12.-LRU-test-results.md).

This was a comparative test of two code versions: one – current main (at hash `68f0e8ff`), another one – current main with fixes from `lru` branch on top of it (see fixes here: https://github.com/t7ko-seagate/cortx-s3server/tree/br/it/EOS-15900-lru).

Goal of the test: see if LRU fix improves TTFB.

Test environment:

*    R1 HW node (server node).
*    Client load was run on the server, not on the separate node.
*    Cluster was started in "dev environment", using s3 team startup scripts.
*    S3 server config is taken as in production.
*    4 Motr IO service instances, 11 s3server instances.
*    Motr was configured to use loopback devices, pointing to local files on
     `/var/motr` (disk storage was NOT used for IO at all).

Test load used for the test:

*    `s3bench` (modified, version as of 2020-04-09)
*    64 parallel sessions (`-numClients 64`)
*    object size 4KB (`-objectSize 4Kb)`
*    256 samples, each sample was read 8 times during read phase, total 2048
     reads (`-numSamples 256 -sampleReads 8`)

Summary:

*    original code takes 500ms on average to load bucket metadata from Motr.
*    with LRU code, this phase takes 80ms on average for load metadata phase.
*    Average TTFB: original 0.593, `lru` 0.305, improvement 2x times.
*    Total read phase duration: original 19.196, `lru` 9.832, improvement 2x times.
*    Conclusion: great result, fix is good and needs to be included to support
     SCALE-80 (TTFB) and SCALE-50 (small objects throughput).

NOTE: these TTFB numbers are NOT what real production deployment will show, this
was a synthetic test with manually deployed dev build. (Production-based
performance test environment is not yet available to S3 team.) The 2x
improvement is ALSO NOT TO BE EXPECTED in real deployment. Motr/S3 configuration
will be different, and so timing may change, including relative timing.


2- Feasibility study
--------------------

Code analysis did not reveal any new issues which make the change impossible.