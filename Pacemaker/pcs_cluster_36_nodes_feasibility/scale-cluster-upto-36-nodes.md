# 36 Node pacemaker cluster experiments

Purposes:
1. Verify pcs cluster supports upto 36 nodes.
2. Validate pcs cluster is stable with 36 nodes.

Experiments:
1. Add nodes up to 36 verify corosync limit and add remote nodes once it exceed corosync limit.
2. Configure the dummy resources with the dependency.
3. Measure network traffic.
4. Performs the basic pcs command and verify the stability of the cluster.
5. Tune cluster property to support large cluster and measure impact on the network traffic and cluster stability.

Outcome:

## 1. Add nodes up to 36 verify corosync limit
- Able to create 36 nodes cluster with 32 normal nodes and 4 remote nodes.
- We created below scripts to create cluster, add normal and remote nodes.
config.sh


## 2. Configure the dummy resources with the dependency
- Configured around 603 resource with the dependecy in the cluster and observed that pcs cluster became unstable. We observed from corosync logs, PCMK_ipc_buffer has exceeded buffer limit and also saw some bad file descriptor related errors.

Solution: We tried below solution and able to get rid of from those errors.
        i. Increased IPC buffer limit (PCMK_ipc_buffer=19725604)
        ii. Increased open file limit to 1048575 (ulimit -n 1048575)

PCS Output after configuring the resources

```
Cluster name: HA_cluster
Stack: corosync
Current DC: srvnode-5 (version 1.1.23-1.el7-9acf116022) - partition with quorum
Last updated: Thu Jan  7 00:22:26 2021
Last change: Wed Jan  6 23:15:19 2021 by root via cibadmin on srvnode-1

36 nodes configured
618 resource instances configured

Online: [ srvnode-1 srvnode-10 srvnode-11 srvnode-12 srvnode-13 srvnode-14 srvnode-15 srvnode-16 srvnode-17 srvnode-18 srvnode-19 srvnode-2 srvnode-20 srvnode-21 srvnode-22 srvnode-23 srvnode-24 srvnode-25 srvnode-26 srvnode-27 srvnode-28 srvnode-29 srvnode-3 srvnode-30 srvnode-31 srvnode-32 srvnode-4 srvnode-5 srvnode-6 srvnode-7 srvnode-8 srvnode-9 ]
RemoteOnline: [ srvnode-33 srvnode-34 srvnode-35 srvnode-36 ]

Full list of resources:

 Clone Set: s3server-clone [s3server] (unique)
     s3server:0 (ocf::seagate:s3server):        Started srvnode-33
     s3server:1 (ocf::seagate:s3server):        Started srvnode-1
     s3server:2 (ocf::seagate:s3server):        Started srvnode-13
     s3server:3 (ocf::seagate:s3server):        Started srvnode-14
     s3server:4 (ocf::seagate:s3server):        Started srvnode-15
     s3server:5 (ocf::seagate:s3server):        Started srvnode-16
     s3server:6 (ocf::seagate:s3server):        Started srvnode-17
     s3server:7 (ocf::seagate:s3server):        Started srvnode-18
     s3server:8 (ocf::seagate:s3server):        Started srvnode-2
     s3server:9 (ocf::seagate:s3server):        Started srvnode-23
     s3server:10        (ocf::seagate:s3server):        Started srvnode-24
     s3server:11        (ocf::seagate:s3server):        Started srvnode-20
     s3server:12        (ocf::seagate:s3server):        Started srvnode-21
     s3server:13        (ocf::seagate:s3server):        Started srvnode-22
     s3server:14        (ocf::seagate:s3server):        Started srvnode-31
     s3server:15        (ocf::seagate:s3server):        Started srvnode-32
     s3server:16        (ocf::seagate:s3server):        Started srvnode-25
     s3server:17        (ocf::seagate:s3server):        Started srvnode-26
     s3server:18        (ocf::seagate:s3server):        Started srvnode-27
     s3server:19        (ocf::seagate:s3server):        Started srvnode-28
     s3server:20        (ocf::seagate:s3server):        Started srvnode-29
     s3server:21        (ocf::seagate:s3server):        Started srvnode-3
     s3server:22        (ocf::seagate:s3server):        Started srvnode-30
     s3server:23        (ocf::seagate:s3server):        Started srvnode-24
     s3server:24        (ocf::seagate:s3server):        Started srvnode-33
     s3server:25        (ocf::seagate:s3server):        Started srvnode-34
     s3server:26        (ocf::seagate:s3server):        Started srvnode-35
     s3server:27        (ocf::seagate:s3server):        Started srvnode-36
     s3server:28        (ocf::seagate:s3server):        Started srvnode-13
     s3server:29        (ocf::seagate:s3server):        Started srvnode-5
     s3server:30        (ocf::seagate:s3server):        Started srvnode-6
     s3server:31        (ocf::seagate:s3server):        Started srvnode-7
     s3server:32        (ocf::seagate:s3server):        Started srvnode-8
     s3server:33        (ocf::seagate:s3server):        Started srvnode-9
     s3server:34        (ocf::seagate:s3server):        Started srvnode-15
     s3server:35        (ocf::seagate:s3server):        Started srvnode-10
     s3server:36        (ocf::seagate:s3server):        Started srvnode-11
     s3server:37        (ocf::seagate:s3server):        Started srvnode-12
     s3server:38        (ocf::seagate:s3server):        Started srvnode-16
     s3server:39        (ocf::seagate:s3server):        Started srvnode-17
     s3server:40        (ocf::seagate:s3server):        Started srvnode-18
     s3server:41        (ocf::seagate:s3server):        Started srvnode-2
     s3server:42        (ocf::seagate:s3server):        Started srvnode-23
     s3server:43        (ocf::seagate:s3server):        Started srvnode-1
     s3server:44        (ocf::seagate:s3server):        Started srvnode-31
     s3server:45        (ocf::seagate:s3server):        Started srvnode-32
     s3server:46        (ocf::seagate:s3server):        Started srvnode-24
     s3server:47        (ocf::seagate:s3server):        Started srvnode-33
     s3server:48        (ocf::seagate:s3server):        Started srvnode-13
     s3server:49        (ocf::seagate:s3server):        Started srvnode-15
     s3server:50        (ocf::seagate:s3server):        Started srvnode-16
     s3server:51        (ocf::seagate:s3server):        Started srvnode-17
     s3server:52        (ocf::seagate:s3server):        Started srvnode-18
     s3server:53        (ocf::seagate:s3server):        Started srvnode-2
     s3server:54        (ocf::seagate:s3server):        Started srvnode-23
     s3server:55        (ocf::seagate:s3server):        Started srvnode-1
     s3server:56        (ocf::seagate:s3server):        Started srvnode-31
     s3server:57        (ocf::seagate:s3server):        Started srvnode-32
     s3server:58        (ocf::seagate:s3server):        Started srvnode-24
     s3server:59        (ocf::seagate:s3server):        Started srvnode-4
     s3server:60        (ocf::seagate:s3server):        Started srvnode-33
     s3server:61        (ocf::seagate:s3server):        Started srvnode-13
     s3server:62        (ocf::seagate:s3server):        Started srvnode-15
     s3server:63        (ocf::seagate:s3server):        Started srvnode-16
     s3server:64        (ocf::seagate:s3server):        Started srvnode-17
     s3server:65        (ocf::seagate:s3server):        Started srvnode-18
     s3server:66        (ocf::seagate:s3server):        Started srvnode-2
     s3server:67        (ocf::seagate:s3server):        Started srvnode-23
     s3server:68        (ocf::seagate:s3server):        Started srvnode-1
     s3server:69        (ocf::seagate:s3server):        Started srvnode-31
     s3server:70        (ocf::seagate:s3server):        Started srvnode-32
     s3server:71        (ocf::seagate:s3server):        Started srvnode-24
     s3server:72        (ocf::seagate:s3server):        Started srvnode-4
     s3server:73        (ocf::seagate:s3server):        Started srvnode-33
     s3server:74        (ocf::seagate:s3server):        Started srvnode-13
     s3server:75        (ocf::seagate:s3server):        Started srvnode-15
     s3server:76        (ocf::seagate:s3server):        Started srvnode-16
     s3server:77        (ocf::seagate:s3server):        Started srvnode-17
     s3server:78        (ocf::seagate:s3server):        Started srvnode-18
     s3server:79        (ocf::seagate:s3server):        Started srvnode-2
     s3server:80        (ocf::seagate:s3server):        Started srvnode-23
     s3server:81        (ocf::seagate:s3server):        Started srvnode-1
     s3server:82        (ocf::seagate:s3server):        Started srvnode-31
     s3server:83        (ocf::seagate:s3server):        Started srvnode-32
     s3server:84        (ocf::seagate:s3server):        Started srvnode-24
     s3server:85        (ocf::seagate:s3server):        Started srvnode-4
     s3server:86        (ocf::seagate:s3server):        Started srvnode-33
     s3server:87        (ocf::seagate:s3server):        Started srvnode-13
     s3server:88        (ocf::seagate:s3server):        Started srvnode-15
     s3server:89        (ocf::seagate:s3server):        Started srvnode-16
     s3server:90        (ocf::seagate:s3server):        Started srvnode-17
     s3server:91        (ocf::seagate:s3server):        Started srvnode-18
     s3server:92        (ocf::seagate:s3server):        Started srvnode-2
     s3server:93        (ocf::seagate:s3server):        Started srvnode-23
     s3server:94        (ocf::seagate:s3server):        Started srvnode-1
     s3server:95        (ocf::seagate:s3server):        Started srvnode-31
     s3server:96        (ocf::seagate:s3server):        Started srvnode-32
     s3server:97        (ocf::seagate:s3server):        Started srvnode-24
     s3server:98        (ocf::seagate:s3server):        Started srvnode-4
     s3server:99        (ocf::seagate:s3server):        Started srvnode-33
     s3server:100       (ocf::seagate:s3server):        Started srvnode-13
     s3server:101       (ocf::seagate:s3server):        Started srvnode-15
     s3server:102       (ocf::seagate:s3server):        Started srvnode-16
     s3server:103       (ocf::seagate:s3server):        Started srvnode-6
     s3server:104       (ocf::seagate:s3server):        Started srvnode-7
     s3server:105       (ocf::seagate:s3server):        Started srvnode-8
     s3server:106       (ocf::seagate:s3server):        Started srvnode-9
     s3server:107       (ocf::seagate:s3server):        Started srvnode-17
     s3server:108       (ocf::seagate:s3server):        Started srvnode-10
     s3server:109       (ocf::seagate:s3server):        Started srvnode-11
     s3server:110       (ocf::seagate:s3server):        Started srvnode-12
     s3server:111       (ocf::seagate:s3server):        Started srvnode-13
     s3server:112       (ocf::seagate:s3server):        Started srvnode-14
     s3server:113       (ocf::seagate:s3server):        Started srvnode-15
     s3server:114       (ocf::seagate:s3server):        Started srvnode-16
     s3server:115       (ocf::seagate:s3server):        Started srvnode-17
     s3server:116       (ocf::seagate:s3server):        Started srvnode-18
     s3server:117       (ocf::seagate:s3server):        Started srvnode-19
     s3server:118       (ocf::seagate:s3server):        Started srvnode-2
     s3server:119       (ocf::seagate:s3server):        Started srvnode-20
     s3server:120       (ocf::seagate:s3server):        Started srvnode-21
     s3server:121       (ocf::seagate:s3server):        Started srvnode-22
     s3server:122       (ocf::seagate:s3server):        Started srvnode-23
     s3server:123       (ocf::seagate:s3server):        Started srvnode-1
     s3server:124       (ocf::seagate:s3server):        Started srvnode-25
     s3server:125       (ocf::seagate:s3server):        Started srvnode-26
     s3server:126       (ocf::seagate:s3server):        Started srvnode-27
     s3server:127       (ocf::seagate:s3server):        Started srvnode-28
     s3server:128       (ocf::seagate:s3server):        Started srvnode-29
     s3server:129       (ocf::seagate:s3server):        Started srvnode-3
     s3server:130       (ocf::seagate:s3server):        Started srvnode-30
     s3server:131       (ocf::seagate:s3server):        Started srvnode-31
     s3server:132       (ocf::seagate:s3server):        Started srvnode-32
     s3server:133       (ocf::seagate:s3server):        Started srvnode-34
     s3server:134       (ocf::seagate:s3server):        Started srvnode-35
     s3server:135       (ocf::seagate:s3server):        Started srvnode-36
     s3server:136       (ocf::seagate:s3server):        Started srvnode-4
     s3server:137       (ocf::seagate:s3server):        Started srvnode-5
     s3server:138       (ocf::seagate:s3server):        Started srvnode-6
     s3server:139       (ocf::seagate:s3server):        Started srvnode-7
     s3server:140       (ocf::seagate:s3server):        Started srvnode-8
     s3server:141       (ocf::seagate:s3server):        Started srvnode-9
     s3server:142       (ocf::seagate:s3server):        Started srvnode-18
     s3server:143       (ocf::seagate:s3server):        Started srvnode-10
     s3server:144       (ocf::seagate:s3server):        Started srvnode-11
     s3server:145       (ocf::seagate:s3server):        Started srvnode-12
     s3server:146       (ocf::seagate:s3server):        Started srvnode-2
     s3server:147       (ocf::seagate:s3server):        Started srvnode-14
     s3server:148       (ocf::seagate:s3server):        Started srvnode-23
     s3server:149       (ocf::seagate:s3server):        Started srvnode-24
     s3server:150       (ocf::seagate:s3server):        Started srvnode-28
     s3server:151       (ocf::seagate:s3server):        Started srvnode-31
     s3server:152       (ocf::seagate:s3server):        Started srvnode-19
     s3server:153       (ocf::seagate:s3server):        Started srvnode-32
     s3server:154       (ocf::seagate:s3server):        Started srvnode-20
     s3server:155       (ocf::seagate:s3server):        Started srvnode-21
     s3server:156       (ocf::seagate:s3server):        Started srvnode-22
     s3server:157       (ocf::seagate:s3server):        Started srvnode-33
     s3server:158       (ocf::seagate:s3server):        Started srvnode-4
     s3server:159       (ocf::seagate:s3server):        Started srvnode-25
     s3server:160       (ocf::seagate:s3server):        Started srvnode-26
     s3server:161       (ocf::seagate:s3server):        Started srvnode-27
     s3server:162       (ocf::seagate:s3server):        Started srvnode-28
     s3server:163       (ocf::seagate:s3server):        Started srvnode-29
     s3server:164       (ocf::seagate:s3server):        Started srvnode-3
     s3server:165       (ocf::seagate:s3server):        Started srvnode-30
     s3server:166       (ocf::seagate:s3server):        Started srvnode-1
     s3server:167       (ocf::seagate:s3server):        Started srvnode-13
     s3server:168       (ocf::seagate:s3server):        Started srvnode-34
     s3server:169       (ocf::seagate:s3server):        Started srvnode-35
     s3server:170       (ocf::seagate:s3server):        Started srvnode-36
     s3server:171       (ocf::seagate:s3server):        Started srvnode-4
     s3server:172       (ocf::seagate:s3server):        Started srvnode-5
     s3server:173       (ocf::seagate:s3server):        Started srvnode-6
     s3server:174       (ocf::seagate:s3server):        Started srvnode-7
     s3server:175       (ocf::seagate:s3server):        Started srvnode-8
     s3server:176       (ocf::seagate:s3server):        Started srvnode-9
     s3server:177       (ocf::seagate:s3server):        Started srvnode-15
     s3server:178       (ocf::seagate:s3server):        Started srvnode-10
     s3server:179       (ocf::seagate:s3server):        Started srvnode-11
     s3server:180       (ocf::seagate:s3server):        Started srvnode-12
     s3server:181       (ocf::seagate:s3server):        Started srvnode-16
     s3server:182       (ocf::seagate:s3server):        Started srvnode-14
     s3server:183       (ocf::seagate:s3server):        Started srvnode-17
     s3server:184       (ocf::seagate:s3server):        Started srvnode-18
     s3server:185       (ocf::seagate:s3server):        Started srvnode-19
     s3server:186       (ocf::seagate:s3server):        Started srvnode-2
     s3server:187       (ocf::seagate:s3server):        Started srvnode-19
     s3server:188       (ocf::seagate:s3server):        Started srvnode-23
     s3server:189       (ocf::seagate:s3server):        Started srvnode-20
     s3server:190       (ocf::seagate:s3server):        Started srvnode-21
     s3server:191       (ocf::seagate:s3server):        Started srvnode-22
     s3server:192       (ocf::seagate:s3server):        Started srvnode-24
     s3server:193       (ocf::seagate:s3server):        Started srvnode-28
     s3server:194       (ocf::seagate:s3server):        Started srvnode-25
     s3server:195       (ocf::seagate:s3server):        Started srvnode-26
     s3server:196       (ocf::seagate:s3server):        Started srvnode-27
     s3server:197       (ocf::seagate:s3server):        Started srvnode-28
     s3server:198       (ocf::seagate:s3server):        Started srvnode-29
     s3server:199       (ocf::seagate:s3server):        Started srvnode-3
     s3server:200       (ocf::seagate:s3server):        Started srvnode-30
     s3server:201       (ocf::seagate:s3server):        Started srvnode-3
     s3server:202       (ocf::seagate:s3server):        Started srvnode-30
     s3server:203       (ocf::seagate:s3server):        Started srvnode-34
     s3server:204       (ocf::seagate:s3server):        Started srvnode-35
     s3server:205       (ocf::seagate:s3server):        Started srvnode-36
     s3server:206       (ocf::seagate:s3server):        Started srvnode-4
     s3server:207       (ocf::seagate:s3server):        Started srvnode-5
     s3server:208       (ocf::seagate:s3server):        Started srvnode-6
     s3server:209       (ocf::seagate:s3server):        Started srvnode-7
     s3server:210       (ocf::seagate:s3server):        Started srvnode-8
     s3server:211       (ocf::seagate:s3server):        Started srvnode-9
     s3server:212       (ocf::seagate:s3server):        Started srvnode-31
     s3server:213       (ocf::seagate:s3server):        Started srvnode-10
     s3server:214       (ocf::seagate:s3server):        Started srvnode-11
     s3server:215       (ocf::seagate:s3server):        Started srvnode-12
     s3server:216       (ocf::seagate:s3server):        Started srvnode-32
     s3server:217       (ocf::seagate:s3server):        Started srvnode-14
     s3server:218       (ocf::seagate:s3server):        Started srvnode-33
     s3server:219       (ocf::seagate:s3server):        Started srvnode-34
     s3server:220       (ocf::seagate:s3server):        Started srvnode-35
     s3server:221       (ocf::seagate:s3server):        Started srvnode-36
     s3server:222       (ocf::seagate:s3server):        Started srvnode-19
     s3server:223       (ocf::seagate:s3server):        Started srvnode-4
     s3server:224       (ocf::seagate:s3server):        Started srvnode-20
     s3server:225       (ocf::seagate:s3server):        Started srvnode-21
     s3server:226       (ocf::seagate:s3server):        Started srvnode-22
     s3server:227       (ocf::seagate:s3server):        Started srvnode-5
     s3server:228       (ocf::seagate:s3server):        Started srvnode-1
     s3server:229       (ocf::seagate:s3server):        Started srvnode-25
     s3server:230       (ocf::seagate:s3server):        Started srvnode-26
     s3server:231       (ocf::seagate:s3server):        Started srvnode-27
     s3server:232       (ocf::seagate:s3server):        Started srvnode-28
     s3server:233       (ocf::seagate:s3server):        Started srvnode-29
     s3server:234       (ocf::seagate:s3server):        Started srvnode-3
     s3server:235       (ocf::seagate:s3server):        Started srvnode-30
     s3server:236       (ocf::seagate:s3server):        Started srvnode-13
     s3server:237       (ocf::seagate:s3server):        Started srvnode-14
     s3server:238       (ocf::seagate:s3server):        Started srvnode-15
     s3server:239       (ocf::seagate:s3server):        Started srvnode-34
     s3server:240       (ocf::seagate:s3server):        Started srvnode-35
     s3server:241       (ocf::seagate:s3server):        Started srvnode-36
     s3server:242       (ocf::seagate:s3server):        Started srvnode-16
     s3server:243       (ocf::seagate:s3server):        Started srvnode-5
     s3server:244       (ocf::seagate:s3server):        Started srvnode-6
     s3server:245       (ocf::seagate:s3server):        Started srvnode-7
     s3server:246       (ocf::seagate:s3server):        Started srvnode-8
     s3server:247       (ocf::seagate:s3server):        Started srvnode-9
     s3server:248       (ocf::seagate:s3server):        Started srvnode-17
     s3server:249       (ocf::seagate:s3server):        Started srvnode-10
     s3server:250       (ocf::seagate:s3server):        Started srvnode-11
     s3server:251       (ocf::seagate:s3server):        Started srvnode-12
     s3server:252       (ocf::seagate:s3server):        Started srvnode-18
     s3server:253       (ocf::seagate:s3server):        Started srvnode-14
     s3server:254       (ocf::seagate:s3server):        Started srvnode-19
     s3server:255       (ocf::seagate:s3server):        Started srvnode-2
     s3server:256       (ocf::seagate:s3server):        Started srvnode-20
     s3server:257       (ocf::seagate:s3server):        Started srvnode-21
     s3server:258       (ocf::seagate:s3server):        Started srvnode-19
     s3server:259       (ocf::seagate:s3server):        Started srvnode-22
     s3server:260       (ocf::seagate:s3server):        Started srvnode-20
     s3server:261       (ocf::seagate:s3server):        Started srvnode-21
     s3server:262       (ocf::seagate:s3server):        Started srvnode-22
     s3server:263       (ocf::seagate:s3server):        Started srvnode-23
     s3server:264       (ocf::seagate:s3server):        Started srvnode-24
     s3server:265       (ocf::seagate:s3server):        Started srvnode-25
     s3server:266       (ocf::seagate:s3server):        Started srvnode-26
     s3server:267       (ocf::seagate:s3server):        Started srvnode-27
     s3server:268       (ocf::seagate:s3server):        Started srvnode-28
     s3server:269       (ocf::seagate:s3server):        Started srvnode-29
     s3server:270       (ocf::seagate:s3server):        Started srvnode-3
     s3server:271       (ocf::seagate:s3server):        Started srvnode-30
     s3server:272       (ocf::seagate:s3server):        Started srvnode-25
     s3server:273       (ocf::seagate:s3server):        Started srvnode-26
     s3server:274       (ocf::seagate:s3server):        Started srvnode-27
     s3server:275       (ocf::seagate:s3server):        Started srvnode-34
     s3server:276       (ocf::seagate:s3server):        Started srvnode-35
     s3server:277       (ocf::seagate:s3server):        Started srvnode-36
     s3server:278       (ocf::seagate:s3server):        Started srvnode-28
     s3server:279       (ocf::seagate:s3server):        Started srvnode-5
     s3server:280       (ocf::seagate:s3server):        Started srvnode-6
     s3server:281       (ocf::seagate:s3server):        Started srvnode-7
     s3server:282       (ocf::seagate:s3server):        Started srvnode-8
     s3server:283       (ocf::seagate:s3server):        Started srvnode-9
     s3server:284       (ocf::seagate:s3server):        Started srvnode-29
     s3server:285       (ocf::seagate:s3server):        Started srvnode-10
     s3server:286       (ocf::seagate:s3server):        Started srvnode-11
     s3server:287       (ocf::seagate:s3server):        Started srvnode-12
     s3server:288       (ocf::seagate:s3server):        Started srvnode-3
     s3server:289       (ocf::seagate:s3server):        Started srvnode-14
     s3server:290       (ocf::seagate:s3server):        Started srvnode-30
     s3server:291       (ocf::seagate:s3server):        Started srvnode-31
     s3server:292       (ocf::seagate:s3server):        Started srvnode-32
     s3server:293       (ocf::seagate:s3server):        Started srvnode-33
     s3server:294       (ocf::seagate:s3server):        Started srvnode-19
     s3server:295       (ocf::seagate:s3server):        Started srvnode-34
     s3server:296       (ocf::seagate:s3server):        Started srvnode-20
     s3server:297       (ocf::seagate:s3server):        Started srvnode-21
     s3server:298       (ocf::seagate:s3server):        Started srvnode-22
     s3server:299       (ocf::seagate:s3server):        Started srvnode-35
     s3server:300       (ocf::seagate:s3server):        Started srvnode-36
     s3server:301       (ocf::seagate:s3server):        Started srvnode-25
     s3server:302       (ocf::seagate:s3server):        Started srvnode-26
     s3server:303       (ocf::seagate:s3server):        Started srvnode-27
     s3server:304       (ocf::seagate:s3server):        Started srvnode-28
     s3server:305       (ocf::seagate:s3server):        Started srvnode-29
     s3server:306       (ocf::seagate:s3server):        Started srvnode-3
     s3server:307       (ocf::seagate:s3server):        Started srvnode-30
     s3server:308       (ocf::seagate:s3server):        Started srvnode-4
     s3server:309       (ocf::seagate:s3server):        Started srvnode-5
     s3server:310       (ocf::seagate:s3server):        Started srvnode-6
     s3server:311       (ocf::seagate:s3server):        Started srvnode-34
     s3server:312       (ocf::seagate:s3server):        Started srvnode-35
     s3server:313       (ocf::seagate:s3server):        Started srvnode-36
     s3server:314       (ocf::seagate:s3server):        Started srvnode-7
     s3server:315       (ocf::seagate:s3server):        Started srvnode-5
     s3server:316       (ocf::seagate:s3server):        Started srvnode-6
     s3server:317       (ocf::seagate:s3server):        Started srvnode-7
     s3server:318       (ocf::seagate:s3server):        Started srvnode-8
     s3server:319       (ocf::seagate:s3server):        Started srvnode-9
     s3server:320       (ocf::seagate:s3server):        Started srvnode-8
     s3server:321       (ocf::seagate:s3server):        Started srvnode-10
     s3server:322       (ocf::seagate:s3server):        Started srvnode-11
     s3server:323       (ocf::seagate:s3server):        Started srvnode-12
     s3server:324       (ocf::seagate:s3server):        Started srvnode-9
     s3server:325       (ocf::seagate:s3server):        Started srvnode-14
     s3server:326       (ocf::seagate:s3server):        Started srvnode-1
     s3server:327       (ocf::seagate:s3server):        Started srvnode-10
     s3server:328       (ocf::seagate:s3server):        Started srvnode-11
     s3server:329       (ocf::seagate:s3server):        Started srvnode-12
     s3server:330       (ocf::seagate:s3server):        Started srvnode-19
     s3server:331       (ocf::seagate:s3server):        Started srvnode-13
     s3server:332       (ocf::seagate:s3server):        Started srvnode-20
     s3server:333       (ocf::seagate:s3server):        Started srvnode-21
     s3server:334       (ocf::seagate:s3server):        Started srvnode-22
     s3server:335       (ocf::seagate:s3server):        Started srvnode-14
     s3server:336       (ocf::seagate:s3server):        Started srvnode-15
     s3server:337       (ocf::seagate:s3server):        Started srvnode-25
     s3server:338       (ocf::seagate:s3server):        Started srvnode-26
     s3server:339       (ocf::seagate:s3server):        Started srvnode-27
     s3server:340       (ocf::seagate:s3server):        Started srvnode-16
     s3server:341       (ocf::seagate:s3server):        Started srvnode-29
     s3server:342       (ocf::seagate:s3server):        Started srvnode-3
     s3server:343       (ocf::seagate:s3server):        Started srvnode-30
     s3server:344       (ocf::seagate:s3server):        Started srvnode-17
     s3server:345       (ocf::seagate:s3server):        Started srvnode-18
     s3server:346       (ocf::seagate:s3server):        Started srvnode-19
     s3server:347       (ocf::seagate:s3server):        Started srvnode-34
     s3server:348       (ocf::seagate:s3server):        Started srvnode-35
     s3server:349       (ocf::seagate:s3server):        Started srvnode-36
     s3server:350       (ocf::seagate:s3server):        Started srvnode-2
     s3server:351       (ocf::seagate:s3server):        Started srvnode-5
     s3server:352       (ocf::seagate:s3server):        Started srvnode-6
     s3server:353       (ocf::seagate:s3server):        Started srvnode-7
     s3server:354       (ocf::seagate:s3server):        Started srvnode-8
     s3server:355       (ocf::seagate:s3server):        Started srvnode-9
     s3server:356       (ocf::seagate:s3server):        Started srvnode-20
     s3server:357       (ocf::seagate:s3server):        Started srvnode-10
     s3server:358       (ocf::seagate:s3server):        Started srvnode-11
     s3server:359       (ocf::seagate:s3server):        Started srvnode-12
     s3server:360       (ocf::seagate:s3server):        Started srvnode-21
     s3server:361       (ocf::seagate:s3server):        Started srvnode-14
     s3server:362       (ocf::seagate:s3server):        Started srvnode-22
     s3server:363       (ocf::seagate:s3server):        Started srvnode-23
     s3server:364       (ocf::seagate:s3server):        Started srvnode-24
     s3server:365       (ocf::seagate:s3server):        Started srvnode-25
     s3server:366       (ocf::seagate:s3server):        Started srvnode-19
     s3server:367       (ocf::seagate:s3server):        Started srvnode-26
     s3server:368       (ocf::seagate:s3server):        Started srvnode-20
     s3server:369       (ocf::seagate:s3server):        Started srvnode-21
     s3server:370       (ocf::seagate:s3server):        Started srvnode-22
     s3server:371       (ocf::seagate:s3server):        Started srvnode-27
     s3server:372       (ocf::seagate:s3server):        Started srvnode-28
     s3server:373       (ocf::seagate:s3server):        Started srvnode-25
     s3server:374       (ocf::seagate:s3server):        Started srvnode-26
     s3server:375       (ocf::seagate:s3server):        Started srvnode-27
     s3server:376       (ocf::seagate:s3server):        Started srvnode-29
     s3server:377       (ocf::seagate:s3server):        Started srvnode-29
     s3server:378       (ocf::seagate:s3server):        Started srvnode-3
     s3server:379       (ocf::seagate:s3server):        Started srvnode-30
     s3server:380       (ocf::seagate:s3server):        Started srvnode-31
     s3server:381       (ocf::seagate:s3server):        Started srvnode-32
     s3server:382       (ocf::seagate:s3server):        Started srvnode-33
     s3server:383       (ocf::seagate:s3server):        Started srvnode-34
     s3server:384       (ocf::seagate:s3server):        Started srvnode-35
     s3server:385       (ocf::seagate:s3server):        Started srvnode-36
     s3server:386       (ocf::seagate:s3server):        Started srvnode-4
     s3server:387       (ocf::seagate:s3server):        Started srvnode-5
     s3server:388       (ocf::seagate:s3server):        Started srvnode-6
     s3server:389       (ocf::seagate:s3server):        Started srvnode-7
     s3server:390       (ocf::seagate:s3server):        Started srvnode-8
     s3server:391       (ocf::seagate:s3server):        Started srvnode-9
     s3server:392       (ocf::seagate:s3server):        Started srvnode-1
     s3server:393       (ocf::seagate:s3server):        Started srvnode-10
     s3server:394       (ocf::seagate:s3server):        Started srvnode-11
     s3server:395       (ocf::seagate:s3server):        Started srvnode-12
 Clone Set: hax-c1-clone [hax-c1]
     Started: [ srvnode-1 srvnode-10 srvnode-11 srvnode-12 srvnode-13 srvnode-14 srvnode-15 srvnode-16 srvnode-17 srvnode-18 srvnode-19 srvnode-2 srvnode-20 srvnode-21 srvnode-22 srvnode-23 srvnode-24 srvnode-25 srvnode-26 srvnode-27 srvnode-28 srvnode-29 srvnode-3 srvnode-30 srvnode-31 srvnode-32 srvnode-33 srvnode-34 srvnode-35 srvnode-36 srvnode-4 srvnode-5 srvnode-6 srvnode-7 srvnode-8 srvnode-9 ]
 Clone Set: motr-clone [motr] (unique)
     motr:0     (ocf::seagate:s3server):        Started srvnode-33
     motr:1     (ocf::seagate:s3server):        Started srvnode-13
     motr:2     (ocf::seagate:s3server):        Started srvnode-14
     motr:3     (ocf::seagate:s3server):        Started srvnode-15
     motr:4     (ocf::seagate:s3server):        Started srvnode-16
     motr:5     (ocf::seagate:s3server):        Started srvnode-17
     motr:6     (ocf::seagate:s3server):        Started srvnode-18
     motr:7     (ocf::seagate:s3server):        Started srvnode-19
     motr:8     (ocf::seagate:s3server):        Started srvnode-2
     motr:9     (ocf::seagate:s3server):        Started srvnode-20
     motr:10    (ocf::seagate:s3server):        Started srvnode-21
     motr:11    (ocf::seagate:s3server):        Started srvnode-22
     motr:12    (ocf::seagate:s3server):        Started srvnode-23
     motr:13    (ocf::seagate:s3server):        Started srvnode-24
     motr:14    (ocf::seagate:s3server):        Started srvnode-25
     motr:15    (ocf::seagate:s3server):        Started srvnode-26
     motr:16    (ocf::seagate:s3server):        Started srvnode-27
     motr:17    (ocf::seagate:s3server):        Started srvnode-28
     motr:18    (ocf::seagate:s3server):        Started srvnode-29
     motr:19    (ocf::seagate:s3server):        Started srvnode-3
     motr:20    (ocf::seagate:s3server):        Started srvnode-30
     motr:21    (ocf::seagate:s3server):        Started srvnode-31
     motr:22    (ocf::seagate:s3server):        Started srvnode-32
     motr:23    (ocf::seagate:s3server):        Started srvnode-34
     motr:24    (ocf::seagate:s3server):        Started srvnode-35
     motr:25    (ocf::seagate:s3server):        Started srvnode-36
     motr:26    (ocf::seagate:s3server):        Started srvnode-4
     motr:27    (ocf::seagate:s3server):        Started srvnode-5
     motr:28    (ocf::seagate:s3server):        Started srvnode-6
     motr:29    (ocf::seagate:s3server):        Started srvnode-7
     motr:30    (ocf::seagate:s3server):        Started srvnode-8
     motr:31    (ocf::seagate:s3server):        Started srvnode-9
     motr:32    (ocf::seagate:s3server):        Started srvnode-1
     motr:33    (ocf::seagate:s3server):        Started srvnode-10
     motr:34    (ocf::seagate:s3server):        Started srvnode-11
     motr:35    (ocf::seagate:s3server):        Started srvnode-12
     motr:36    (ocf::seagate:s3server):        Started srvnode-13
     motr:37    (ocf::seagate:s3server):        Started srvnode-14
     motr:38    (ocf::seagate:s3server):        Started srvnode-15
     motr:39    (ocf::seagate:s3server):        Started srvnode-16
     motr:40    (ocf::seagate:s3server):        Started srvnode-17
     motr:41    (ocf::seagate:s3server):        Started srvnode-18
     motr:42    (ocf::seagate:s3server):        Started srvnode-19
     motr:43    (ocf::seagate:s3server):        Started srvnode-2
     motr:44    (ocf::seagate:s3server):        Started srvnode-20
     motr:45    (ocf::seagate:s3server):        Started srvnode-21
     motr:46    (ocf::seagate:s3server):        Started srvnode-22
     motr:47    (ocf::seagate:s3server):        Started srvnode-23
     motr:48    (ocf::seagate:s3server):        Started srvnode-24
     motr:49    (ocf::seagate:s3server):        Started srvnode-25
     motr:50    (ocf::seagate:s3server):        Started srvnode-26
     motr:51    (ocf::seagate:s3server):        Started srvnode-27
     motr:52    (ocf::seagate:s3server):        Started srvnode-28
     motr:53    (ocf::seagate:s3server):        Started srvnode-29
     motr:54    (ocf::seagate:s3server):        Started srvnode-3
     motr:55    (ocf::seagate:s3server):        Started srvnode-30
     motr:56    (ocf::seagate:s3server):        Started srvnode-31
     motr:57    (ocf::seagate:s3server):        Started srvnode-32
     motr:58    (ocf::seagate:s3server):        Started srvnode-33
     motr:59    (ocf::seagate:s3server):        Started srvnode-34
     motr:60    (ocf::seagate:s3server):        Started srvnode-35
     motr:61    (ocf::seagate:s3server):        Started srvnode-36
     motr:62    (ocf::seagate:s3server):        Started srvnode-4
     motr:63    (ocf::seagate:s3server):        Started srvnode-5
     motr:64    (ocf::seagate:s3server):        Started srvnode-6
     motr:65    (ocf::seagate:s3server):        Started srvnode-7
     motr:66    (ocf::seagate:s3server):        Started srvnode-8
     motr:67    (ocf::seagate:s3server):        Started srvnode-9
     motr:68    (ocf::seagate:s3server):        Started srvnode-1
     motr:69    (ocf::seagate:s3server):        Started srvnode-10
     motr:70    (ocf::seagate:s3server):        Started srvnode-11
     motr:71    (ocf::seagate:s3server):        Started srvnode-12
 Clone Set: io_health_path-clone [io_health_path]
     Started: [ srvnode-1 srvnode-10 srvnode-11 srvnode-12 srvnode-13 srvnode-14 srvnode-15 srvnode-16 srvnode-17 srvnode-18 srvnode-19 srvnode-2 srvnode-20 srvnode-21 srvnode-22 srvnode-23 srvnode-24 srvnode-25 srvnode-26 srvnode-27 srvnode-28 srvnode-29 srvnode-3 srvnode-30 srvnode-31 srvnode-32 srvnode-33 srvnode-34 srvnode-35 srvnode-36 srvnode-4 srvnode-5 srvnode-6 srvnode-7 srvnode-8 srvnode-9 ]
 Clone Set: haproxy-clone [haproxy]
     Started: [ srvnode-1 srvnode-10 srvnode-11 srvnode-12 srvnode-13 srvnode-14 srvnode-15 srvnode-16 srvnode-17 srvnode-18 srvnode-19 srvnode-2 srvnode-20 srvnode-21 srvnode-22 srvnode-23 srvnode-24 srvnode-25 srvnode-26 srvnode-27 srvnode-28 srvnode-29 srvnode-3 srvnode-30 srvnode-31 srvnode-32 srvnode-33 srvnode-34 srvnode-35 srvnode-36 srvnode-4 srvnode-5 srvnode-6 srvnode-7 srvnode-8 srvnode-9 ]
 Clone Set: s3auth-clone [s3auth]
     Started: [ srvnode-1 srvnode-10 srvnode-11 srvnode-12 srvnode-13 srvnode-14 srvnode-15 srvnode-16 srvnode-17 srvnode-18 srvnode-19 srvnode-2 srvnode-20 srvnode-21 srvnode-22 srvnode-23 srvnode-24 srvnode-25 srvnode-26 srvnode-27 srvnode-28 srvnode-29 srvnode-3 srvnode-30 srvnode-31 srvnode-32 srvnode-33 srvnode-34 srvnode-35 srvnode-36 srvnode-4 srvnode-5 srvnode-6 srvnode-7 srvnode-8 srvnode-9 ]
 csm    (ocf::heartbeat:Dummy): Started srvnode-14
 mgmt_health_path       (ocf::heartbeat:Dummy): Started srvnode-14
 srvnode-33     (ocf::pacemaker:remote):        Started srvnode-1
 srvnode-34     (ocf::pacemaker:remote):        Started srvnode-11
 srvnode-35     (ocf::pacemaker:remote):        Started srvnode-12
 srvnode-36     (ocf::pacemaker:remote):        Started srvnode-13

Daemon Status:
  corosync: active/enabled
  pacemaker: active/enabled
  pcsd: active/enabled
```


## 3. Measure network traffic

Without any operation network traffic

```
Incoming:
        Curr: 1.54 kBit/s
        Avg: 2.74 kBit/s
        Min: 472.00 Bit/s
        Max: 40.59 kBit/s
        Ttl: 2.60 GByte
Outgoing:
        Curr: 328.00 Bit/s
        Avg: 3.04 kBit/s
        Min: 0.00 Bit/s
        Max: 44.96 kBit/s
        Ttl: 4.07 GByte
```

Moving two nodes into standby mode

```
Incoming:
        Curr: 2.84 kBit/s
        Avg: 9.14 kBit/s
        Min: 472.00 Bit/s
        Max: 1.33 MBit/s
        Ttl: 2.60 GByte
Outgoing:
        Curr: 0.00 Bit/s
        Avg: 16.82 kBit/s
        Min: 0.00 Bit/s
        Max: 2.23 MBit/s
        Ttl: 4.07 GByte
```

Moving two nodes into unstandby mode

```
Incoming:
        Curr: 10.36 kBit/s
        Avg: 17.29 kBit/s
        Min: 472.00 Bit/s
        Max: 401.16 kBit/s
        Ttl: 2.60 GByte
Outgoing:
        Curr: 18.60 kBit/s
        Avg: 81.29 kBit/s
        Min: 0.00 Bit/s
        Max: 1.80 MBit/s
        Ttl: 4.07 GByte
```

## 4. Performs the basic pcs command and verify the stability of the cluster
   i. pcs status
    - We observed that "pcs status" command is taking bit more time around 10 sec to 13 sec for the execution.
    - We figured out some other alternatives to get nodes and resources status which are much faster than "pcs status".
        i. pcs status nodes -> Returns the status of all the nodes including remote nodes which are present in the cluster. It took around 1-2 secs for the execution.
        ii. pcs resource -> Returns the resource status of the cluster. It took around 1-2 secs for the execution.

    ii. pcs cluster standby --all
    - We observed pretty much high traffic around XX Mbps on the network when we perform the standby for all the nodes of the cluster.
    - Also observed that some services failed due to timeout.

    Solution: 
    - We increased stop/start timeout from 20 sec to 50 sec but it did not help to fix the issue.
    - We divided all the nodes in the group of three and performed granularly standby like move to next 3 nodes once all the resounces of the first three nodes move to stopped state and it went well. All the services stopped properly.
    - We used below script to automate the operations.

    iii. pcs cluster unstandby --all
    - We observed same behaviour like standby operation. We divided nodes in the group and able to performs unstandby operation succesfully.

## 5. Tune cluster property to support large cluster and measure impact on the network traffic and cluster stability
    - We tuned below property to see impact on the cluster performance.

**Batch-limit** - The maximum number of actions that the cluster may execute in parallel across all nodes. The "correct" value will depend on the speed and load of your network and cluster nodes. If zero, the cluster will impose a dynamically calculated limit only when any node has high load.

**cluster-ipc-limit** - 500	The maximum IPC message backlog before one cluster daemon will disconnect another. This is of use in large clusters, for which a good value is the number of resources in the cluster multiplied by the number of nodes. The default of 500 is also the minimum. Raise this if you see "Evicting client" messages for cluster daemon PIDs in the logs.

    i. Batch-limit - 0 and cluster-ipc-limit - 500
    - Outgoing traffic - 1.43 MBit/s Avg, 5.87 MBit/s Max
    - Incoming traffic - 219.55 kBit/s Avg, 1.77 MBit/s Max

    ii Batch-limit - 25 and cluster-ipc-limit - 10000
    - Outgoing traffic - 725.84 kBit/s Avg, 347.45 MBit/s Max
    - Incoming traffic - 1.14 MBit/s Avg, 47.00 MBit/s Max

    - Observed some services got failed during granularly unstandby operation. 

    iii. Batch-limit - 0 and cluster-ipc-limit - 10000
    - Outgoing traffic - 627.52 kBit/s Avg, 6.25 MBit/s Max
    - Incoming traffic - 134.63 kBit/s Avg, 1.40 MBit/s Max
