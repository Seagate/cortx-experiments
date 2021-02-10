- [Report for Logs size PoC](#orgdc8c064)
- [Search through 2 NFS servers: Puny Longmorn](#org49a44c9)
  - [<http://ssc-nfs-server1.colo.seagate.com/logs1/>](#orgea0b083)
  - [<http://ssc-nfs-srvr2.pun.seagate.com/>](#org3df1d22)
  - [Result: big support bundles > 200M](#orgd6f34d1)
- [Pick several support bundles and check whether they have big amount of HA logs](#org730d5b5)
  - [<http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-14767/secondary/SUPPORT_BUNDLE.SB36w38ubm;546630862>](#org1a9afa8)
  - [<http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-15325/build532/secondary/SUPPORT_BUNDLE.SB1x0duu69o>](#org025226f)
  - [<http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/certification/Node-1/SUPPORT_BUNDLE.SBeiyo8xuq>](#org4f58025)
  - [<http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-16253/live_node/SUPPORT_BUNDLE.SBsifj5q2r;925553016>](#org1b2f86d)
- [corosync.log size reduction options](#org7453cab)
  - [Initial number of lines: 127K, Size: 19M](#org5f8812f)
  - [sed -E /fence\_ipmilan.\*stderr/d gives 127K -> 94K: -5MiB](#org16d3e6d)
  - [sed -E /common\_print/d gives 94K -> 76K: -3MiB](#org4e34f99)
  - [sed -E /cib:/d gives 76K -> 58K: -3.2MiB](#orgc5aa218)
  - [Generic solution: reduce size of logs in logrotate](#orge26a742)
  - [Pacemaker logging options](#org5b2a372)
  - [Summary:](#org3c8438a)
- [Summary](#org0589f57)
  - [Though current existing HA support bundles do not exceed the limit (5MiB) yet - it is just a matter of time taking into accound projected number of nodes in the cluster](#orgba53185)
  - [Taking the mean of 2 forecass (10 days and 2 days), make sense to take 6 days as truncate limit](#org8264969)
  - [Need to implement logrotate mechanism in cortx-ha repo truncating logs after 6 days since it is not implemented](#org216092d)
  - [fence\_ipmi logs can be disabled close to release phase to save some space. So far, they may be quite useful debugging fencing issues.](#orgc946a1f)
  - [Since support bundle is generated ondemand, HA support bundle script can implement some advanced logic for filtering out required logs to include only logs where errors are indicated.](#org322bb19)


<a id="orgdc8c064"></a>

# Report for Logs size PoC



<a id="org49a44c9"></a>

## Search through 2 NFS servers: Puny Longmorn


<a id="orgea0b083"></a>

### <http://ssc-nfs-server1.colo.seagate.com/logs1/>


<a id="org3df1d22"></a>

### <http://ssc-nfs-srvr2.pun.seagate.com/>


<a id="orgd6f34d1"></a>

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


<a id="org730d5b5"></a>

## Pick several support bundles and check whether they have big amount of HA logs


<a id="org1a9afa8"></a>

### <http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-14767/secondary/SUPPORT_BUNDLE.SB36w38ubm;546630862>

1.  500KB HA

    1.  13M
    
        1.  12M corosync.log
        
            -   Nov 26 19:01:09
            -   Nov 27 16:26:59
            -   2 node cluster
        
        2.  634KB pcsd.log
        
        3.  400KB other HA logs
    
    2.  570K/24h which gives us almost 20M for 36 nodes and provides 10 days for logs before they can be truncated.
    
        1.  This is quite an optimistic forecast since most likely logs size grouth is not linear


<a id="org025226f"></a>

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
    
    2.  1M / 9h -> 2.6M/24h
    
        1.  This gives us 2 days of logs approximately
        
        2.  Though, these logs are quite intensive and do not correspond to normal cluster work - it is a worst case
    
    3.  Other logs are not considered due to minimal impact to the support bundle size


<a id="org4f58025"></a>

### <http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/certification/Node-1/SUPPORT_BUNDLE.SBeiyo8xuq>

1GB  

1.  28K HA

    Doesn't make sense to check  


<a id="org1b2f86d"></a>

### <http://ssc-nfs-srvr2.pun.seagate.com/logs1/ldr-r1/EOS-16253/live_node/SUPPORT_BUNDLE.SBsifj5q2r;925553016>

900M  


<a id="org7453cab"></a>

## corosync.log size reduction options

Since that file consumes major part of disk space in support bunle, lets check which options do we have to optimize the size.  


<a id="org5f8812f"></a>

### Initial number of lines: 127K, Size: 19M


<a id="org16d3e6d"></a>

### sed -E /fence\_ipmilan.\*stderr/d gives 127K -> 94K: -5MiB

This can be disabled in fence\_ipmilan configuration for sure.  


<a id="org4e34f99"></a>

### sed -E /common\_print/d gives 94K -> 76K: -3MiB

Need to research whether common\_prints caused by \`pcs status\` invocations can be disabled via pacemaker configuration  


<a id="orgc5aa218"></a>

### sed -E /cib:/d gives 76K -> 58K: -3.2MiB

CIB updates is not really interesing information for analysis, but I would not recommend to remove it from logs  


<a id="orge26a742"></a>

### Generic solution: reduce size of logs in logrotate

1.  In scope of curent PoC logrotate configuration for corosync.log was not found

    Either it is implemented in too generic and grep-resistant way, or it is just missing.  
    Hare component code don't have corosync.log logrotate configuration anymore due to different scope of responsibility - this is expected and understandable.  


<a id="org5b2a372"></a>

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


<a id="org3c8438a"></a>

### Summary:

1.  Up to 8M (42%) can be saved by selecting wich type of logs can disabled


<a id="org0589f57"></a>

## Summary


<a id="orgba53185"></a>

### Though current existing HA support bundles do not exceed the limit (5MiB) yet - it is just a matter of time taking into accound projected number of nodes in the cluster


<a id="org8264969"></a>

### Taking the mean of 2 forecass (10 days and 2 days), make sense to take 6 days as truncate limit


<a id="org216092d"></a>

### Need to implement logrotate mechanism in cortx-ha repo truncating logs after 6 days since it is not implemented


<a id="orgc946a1f"></a>

### fence\_ipmi logs can be disabled close to release phase to save some space. So far, they may be quite useful debugging fencing issues.


<a id="org322bb19"></a>

### Since support bundle is generated ondemand, HA support bundle script can implement some advanced logic for filtering out required logs to include only logs where errors are indicated.
