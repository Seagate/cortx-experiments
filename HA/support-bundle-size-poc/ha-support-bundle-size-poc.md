- [Report for Logs size PoC](#org18eaf45)
  - [Search through 2 NFS servers: Puny Longmorn](#org7a6f910)
    - [<http://ssc-nfs-server1.colo.seagate.com/logs1/>](#orge31c0d8)
    - [<http://ssc-nfs-srvr2.pun.seagate.com/>](#orgeafc31f)
    - [Result: big support bundles > 200M](#org64fb7b2)
  - [Pick several support bundles and check whether they have big amount of HA logs](#org40be316)
    - [<http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-14767/secondary/SUPPORT_BUNDLE.SB36w38ubm;546630862>](#org4d5cff8)
    - [<http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-15325/build532/secondary/SUPPORT_BUNDLE.SB1x0duu69o>](#org8aadcd5)
    - [<http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/certification/Node-1/SUPPORT_BUNDLE.SBeiyo8xuq>](#orgc0ba216)
    - [<http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-16253/live_node/SUPPORT_BUNDLE.SBsifj5q2r;925553016>](#org2546d83)
  - [corosync.log size reduction options](#org465ec25)
    - [Initial number of lines: 127K, Size: 19M](#org1c78c99)
    - [sed -E /fence\_ipmilan.\*stderr/d gives 127K -> 94K: -5MiB](#org6399097)
    - [sed -E /common\_print/d gives 94K -> 76K: -3MiB](#org2f3dcbb)
    - [sed -E /cib:/d gives 76K -> 58K: -3.2MiB](#orgd0f8eca)
    - [Generic solution: reduce size of logs in logrotate](#org61b6731)
    - [Pacemaker logging options](#org83a2bf1)
    - [Summary:](#org13d58e0)
  - [What is missing in current PoC](#org3b2350a)
    - [Need to analyze support bundle for the server with long uptime and without problems](#orgcad6a2b)


<a id="org18eaf45"></a>

# Report for Logs size PoC



<a id="org7a6f910"></a>

## Search through 2 NFS servers: Puny Longmorn


<a id="orge31c0d8"></a>

### <http://ssc-nfs-server1.colo.seagate.com/logs1/>


<a id="orgeafc31f"></a>

### <http://ssc-nfs-srvr2.pun.seagate.com/>


<a id="org64fb7b2"></a>

### Result: big support bundles > 200M

```
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/146_FTEFail/SUPPORT_BUNDLE.SBg8qzxvbl;889683815
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-14064/SUPPORT_BUNDLE.SBe3tfscka;324864313
%RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-14767/secondary/SUPPORT_BUNDLE.SB36w38ubm;546630862
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-15325/build532/secondary/SUPPORT_BUNDLE.SB1x0duu69;327484930
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-15325/primary/SUPPORT_BUNDLE.SBbw5shm64;308201173
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-15325/secondary/SUPPORT_BUNDLE.SBbw5shm64;473134289
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-15329/primary/SUPPORT_BUNDLE.SB19x7areq;354417438
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-16253/live_node/SUPPORT_BUNDLE.SBsifj5q2r;925553016
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-16253/replaced_node/SUPPORT_BUNDLE.SBsifj5q2r;522796323
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-16724/SUPPORT_BUNDLE.SBliepw7u6;1226744925
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/certification/Node-1/SUPPORT_BUNDLE.SBeiyo8xuq;1023115234
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/certification/Node-2/SUPPORT_BUNDLE.SBeiyo8xuq;993653709
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/ldap_issueNode1/SUPPORT_BUNDLE.SBf4iqj4d4;352137341
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/no_hw_alerts_471/SUPPORT_BUNDLE.SBov274tip;356511467
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/node_standby_issue/SUPPORT_BUNDLE.SBko2ygk54;351114297
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/test_6250_failure/SUPPORT_BUNDLE.SB6cjky158;358191304
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/test_8351_B515/SUPPORT_BUNDLE.SBlq0755qi;309143137
RESULT;http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/test_8351_B515/SUPPORT_BUNDLE.SBnc6j2xmv;310950479
```


<a id="org40be316"></a>

## Pick several support bundles and check whether they have big amount of HA logs


<a id="org4d5cff8"></a>

### <http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-14767/secondary/SUPPORT_BUNDLE.SB36w38ubm;546630862>

1.  500KB HA

    1.  13M
    
        1.  12M corosync.log
        
            -   Nov 26 19:01:09
            -   Nov 27 16:26:59
            -   2 node cluster
        
        2.  634KB pcsd.log


<a id="org8aadcd5"></a>

### <http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-15325/build532/secondary/SUPPORT_BUNDLE.SB1x0duu69o>

1.  1M HA

    ```
    total 1.1M
    1640262545 drwx------ 3 744354 744354   73 Feb  7 12:41 ha_SB1x0duu69
    3233635359 -rw-r--r-- 1 744354 744354 1.1M Nov 28 21:10 ha_SB1x0duu69.tar.gz
    
    ./ha_SB1x0duu69:
    total 19M
    2162752323 drwxrwxr-x 2 744354 744354  141 Nov 28 21:10 ha
    1640262548 -rw-rw---- 1 744354 744354  19M Nov 28 21:10 corosync.log
    1640262547 -rw-rw---- 1 744354 744354    0 Nov 28 12:01 pacemaker.log
    1640262546 -rw------- 1 744354 744354 121K Nov 28 21:05 pcsd.log
    
    ./ha_SB1x0duu69/ha:
    total 196K
    2162752324 -rw-r--r-- 1 744354 744354  22K Nov 28 21:10 cortxha.log
    2162752325 -rw-r--r-- 1 744354 744354 5.1K Nov 28 21:10 ha_cmds_output
    2162752329 -rw-rwxr-- 1 744354 744354 2.1K Nov 28 10:02 ha_setup.log
    2162752328 -rw-r----- 1 744354 744354 132K Nov 28 21:01 pcmk_alert.log
    2162752327 -rw-r----- 1 744354 744354  27K Nov 28 20:33 resource_agent.log
    2162752330 -rw-r--r-- 1 744354 744354    0 Nov 28 21:10 support_bundle.err
    ```
    
    1.  19M corosync.log
    
        -   Nov 29 00:31:07
        -   Nov 29 09:40:36
        -   2 node cluster
        
        1.  huge amount of fence\_ipmilan mesages (enabled recently to have information about fencing agent behavior)
        
            Logging configuration shall be revised or logs shall be disabled  


<a id="orgc0ba216"></a>

### <http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/certification/Node-1/SUPPORT_BUNDLE.SBeiyo8xuq>

1GB  

1.  28K HA

    Doesn't make sense to check  


<a id="org2546d83"></a>

### <http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-16253/live_node/SUPPORT_BUNDLE.SBsifj5q2r;925553016>

900M  

1.  


<a id="org465ec25"></a>

## corosync.log size reduction options

Since that file consumes major part of disk space in support bunle, lets check which options do we have to optimize the size.  


<a id="org1c78c99"></a>

### Initial number of lines: 127K, Size: 19M


<a id="org6399097"></a>

### sed -E /fence\_ipmilan.\*stderr/d gives 127K -> 94K: -5MiB

This can be disabled in fence\_ipmilan configuration for sure.  


<a id="org2f3dcbb"></a>

### sed -E /common\_print/d gives 94K -> 76K: -3MiB

Need to research whether common\_prints caused by \`pcs status\` invocations can be disabled via pacemaker configuration  


<a id="orgd0f8eca"></a>

### sed -E /cib:/d gives 76K -> 58K: -3.2MiB

CIB updates is not really interesing information for analysis, but I would not recommend to remove it from logs  


<a id="org61b6731"></a>

### Generic solution: reduce size of logs in logrotate


<a id="org83a2bf1"></a>

### Pacemaker logging options

1.  Configured in corosync.conf

    <https://linux.die.net/man/5/corosync.conf>  
    
    1.  logfile\_priority
    
        This specifies the logfile priority for this particular subsystem. Ignored if debug is on. Possible values are: alert, crit, debug (same as debug = on), emerg, err, info, notice, warning.  
        The default is: info.  
        
        1.  info logs contain pengine decisions which are the main source of information about pacemaker behavior
        
        2.  info logs contain attribute updates which are important if CIB attributes are used in cluster configuration. Valid for LR1, may be valid for LR2.
    
    2.  debug
    
        This specifies whether debug output is logged for this particular logger. Also can contain value trace, what is highest level of debug informations.  
        
        The default is off.  
    
    3.  to\_logfile, to\_syslog, to\_stderr
    
        These specify the destination of logging output. Any combination of these options may be specified. Valid options are yes and no.  
        The default is syslog and stderr.  
        
        Please note, if you are using to\_logfile and want to rotate the file, use logrotate(8) with the option copytruncate. eg.  
        
        ```
        /var/log/corosync.log {
        missingok
        compress
        notifempty
        daily
        rotate 7
        copytruncate
        }
        ```


<a id="org13d58e0"></a>

### Summary:

1.  Up to 8M (42%) can be saved by selecting wich type of logs can disabled


<a id="org3b2350a"></a>

## What is missing in current PoC


<a id="orgcad6a2b"></a>

### Need to analyze support bundle for the server with long uptime and without problems

Different problems in the cluster (migrations, fencing actions, server restarts) produce big amount of logs.  
Make sense to check how many logs are generated during normal operation.
