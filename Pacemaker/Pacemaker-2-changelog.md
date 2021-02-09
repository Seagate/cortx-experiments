- [Differences between Pacemaker 1.1 and 2.0](#org31d2d10)
  - [Generic points:](#orgbd42bfc)
    - [2.0 breaks rolling upgrades from Pacemaker 1.1.10 and earlier on corosync 2 and greater (and of course from any version on other stacks)](#orga3109e6)
    - [Only 2.0 will be actively developed from this point, but at least some bug fixes will be backported to the 1.1 branch for the foreseeable future, and we will eventually do at least one more 1.1 release with those fixes](#org324eeee)
    - [Env variables removed:](#orgb9a68b8)
    - [When Pacemaker or Pacemaker Remote is launched by systemd, by default it will now run without limits on the number of processes it can spawn simultaneously. To override this behavior, create a unit file override for pacemaker.service with TasksMax set to the desired value.](#orgf9c5ff5)
    - [Big amount of options are just renamed. Details are listed in specifc sections.](#org7d60ad9)
    - [Pacemaker daemons are renamed - this can affect scripts that analyze corosync.log or system journal files.](#org1b58193)
    - [crm\_\* prefixed tool's options have been changed. Does not affect R1 or R2.](#orgacdb997)
    - [API changes - then don't look like relevant for R1 or R2 needs](#orga6cfaec)
  - [CIB XML](#orgf99516c)
    - [Deprecated syntax that has been removed](#orgaba23ba)
  - [Clone resources](#orge290e5b)
    - [The resource type referred to as "master/slave", "stateful", or "multi-state" is no longer a separate resource type, but a variation of clone now referred to as a "promotable clone". "Master scores" are now referred to as "promotion scores" (though the names of the crm\_master tool and master-\* node attributes are unchanged)](#org1cec92b)
  - [Cluster properties renamed - this affects existing and new scripts](#org4dc3185)
  - [Resource meta attributes renamed - this affects existing and new scripts](#org78b8ab8)
  - [Operation meta attributes - not used in R1. May affect new scripts for R2.](#orgc1b54a2)
  - [Fence device attributes - this affects exsiting and new scripts](#org7da57b2)
  - [Pacemaker utilities (tools)](#orgd9e5156)
    - [crm\_resource](#org649a4a1)
    - [Changes in other utilities does not affect R1 or R2](#orgb29e273)
  - [The summary of changes between 1.1 and 2.0 versions relevant for R1, R2 releases:](#orge8ebad7)
    - [Cluster objects attributes renamed](#orge980bc6)
    - [Tool changes](#org428b19c)
    - [CIB XML](#orgeaafc00)
    - [Deprecated syntax can't be used since support will be dropped after some 2.0.X release](#org923991a)


<a id="org31d2d10"></a>

# Differences between Pacemaker 1.1 and 2.0


<a id="orgbd42bfc"></a>

## Generic points:

They don't have direct effect to R1 or R2, but worth mention.  


<a id="orga3109e6"></a>

### 2.0 breaks rolling upgrades from Pacemaker 1.1.10 and earlier on corosync 2 and greater (and of course from any version on other stacks)


<a id="org324eeee"></a>

### Only 2.0 will be actively developed from this point, but at least some bug fixes will be backported to the 1.1 branch for the foreseeable future, and we will eventually do at least one more 1.1 release with those fixes


<a id="orgb9a68b8"></a>

### Env variables removed:

LRMD\_MAX\_CHILDREN (use PCMK\_node\_action\_limit instead)  
PCMK\_debugfile and HA\_debugfile (use PCMK\_logfile instead)  
PCMK\_legacy  
PCMK\_STACK  
PCMK\_uname\_is\_uuid  
PCMK\_use\_logd, HA\_use\_logd, and HA\_LOGD (along with the ability to launch pacemaker-mgmtd)  


<a id="orgf9c5ff5"></a>

### When Pacemaker or Pacemaker Remote is launched by systemd, by default it will now run without limits on the number of processes it can spawn simultaneously. To override this behavior, create a unit file override for pacemaker.service with TasksMax set to the desired value.


<a id="org7d60ad9"></a>

### Big amount of options are just renamed. Details are listed in specifc sections.


<a id="org1b58193"></a>

### Pacemaker daemons are renamed - this can affect scripts that analyze corosync.log or system journal files.

Details: <https://wiki.clusterlabs.org/wiki/Pacemaker_2.0_Daemon_Changes#New_names>  

-   attrd -> pacemaker-attrd
-   cib -> pacemaker-based
-   crmd -> pacemaker-controld
-   lrmd -> pacemaker-execd
-   stonithd -> pacemaker-fenced
-   pacemaker\_remoted -> pacemaker-remoted
-   pengine -> pacemaker-schedulerd


<a id="orgacdb997"></a>

### crm\_\* prefixed tool's options have been changed. Does not affect R1 or R2.

Details: <https://wiki.clusterlabs.org/wiki/Pacemaker_2.0_Tool_Changes#Removals>  


<a id="orga6cfaec"></a>

### API changes - then don't look like relevant for R1 or R2 needs

Details: <https://wiki.clusterlabs.org/wiki/Pacemaker_2.0_API_Changes>  


<a id="orgf99516c"></a>

## CIB XML


<a id="orgaba23ba"></a>

### Deprecated syntax that has been removed

1.  This can affect pcswrap implementation and other scripts that parse CIB XML. However the changes does not look relevant for R1 or R2 needs.

2.  Details:

    <https://wiki.clusterlabs.org/wiki/Pacemaker_2.0_Configuration_Changes#Deprecated_syntax_that_has_been_removed>  


<a id="orge290e5b"></a>

## Clone resources


<a id="org1cec92b"></a>

### The resource type referred to as "master/slave", "stateful", or "multi-state" is no longer a separate resource type, but a variation of clone now referred to as a "promotable clone". "Master scores" are now referred to as "promotion scores" (though the names of the crm\_master tool and master-\* node attributes are unchanged)

<https://wiki.clusterlabs.org/wiki/Pacemaker_2.0_Configuration_Changes>  

1.  Clones are used. Promotable clones may be used in R2 as well.

2.  This affects rule writing (most likely)

3.  BUT: The deprecated syntax will continue to be accepted for at least the lifetime of the 2.0.x series.

    This may create a problem after "one more regular pacemaker upgrade" if rules with deprecated syntax will be still in use by that time.  


<a id="org4dc3185"></a>

## Cluster properties renamed - this affects existing and new scripts

-   cluster\_recheck\_interval -> cluster-recheck-interval
-   dc\_deadtime -> dc-deadtime
-   default-action-timeout -> timeout in op\_defaults
-   default\_action\_timeout -> timeout in op\_defaults
-   default-resource-failure-stickiness -> comparable migration-threshold in rsc\_defaults
-   default\_resource\_failure\_stickiness -> comparable migration-threshold in rsc\_defaults
-   default-resource-stickiness -> resource-stickiness in rsc\_defaults
-   default\_resource\_stickiness -> resource-stickiness in rsc\_defaults
-   election\_timeout -> election-timeout
-   expected-quorum-votes -> n/a
-   is-managed-default -> is-managed in rsc\_defaults
-   is\_managed\_default -> is-managed in rsc\_defaults
-   no\_quorum\_policy -> no-quorum-policy
-   remove\_after\_stop -> remove-after-stop
-   shutdown\_escalation -> shutdown-escalation
-   startup\_fencing -> startup-fencing
-   stonith\_action -> stonith-action
-   stonith\_enabled -> stonith-enabled
-   stop\_orphan\_actions -> stop-orphan-actions
-   stop\_orphan\_resources -> stop-orphan-resources
-   symmetric\_cluster -> symmetric-cluster
-   transition\_idle\_timeout -> cluster-delay


<a id="org78b8ab8"></a>

## Resource meta attributes renamed - this affects existing and new scripts

-   isolation, isolation-host, isolation-instance, isolation-wrapper -> bundle resources
-   resource-failure-stickiness -> comparable migration-threshold
-   resource\_failure\_stickiness -> comparable migration-threshold


<a id="orgc1b54a2"></a>

## Operation meta attributes - not used in R1. May affect new scripts for R2.

-   requires -> requires in resource meta-attributes


<a id="org7da57b2"></a>

## Fence device attributes - this affects exsiting and new scripts

-   pcmk\_arg\_map -> comparable pcmk\_host\_argument
-   pcmk\_list\_cmd -> pcmk\_list\_action
-   pcmk\_monitor\_cmd -> pcmk\_monitor\_action
-   pcmk\_off\_cmd -> pcmk\_off\_action
-   pcmk\_on\_cmd -> pcmk\_on\_action
-   pcmk\_poweroff\_action -> pcmk\_off\_action
-   pcmk\_reboot\_cmd -> pcmk\_reboot\_action
-   pcmk\_status\_cmd -> pcmk\_status\_action


<a id="orgd9e5156"></a>

## Pacemaker utilities (tools)


<a id="org649a4a1"></a>

### crm\_resource

1.  The &#x2013;cleanup option now cleans up only resources with failures; the previous behavior of cleaning up all resources can still be achieved with the &#x2013;refresh option.

    This may affect support instructions for R1, but so far it doesn't look so, because only failed resources cleanup is generally needed and this effect is preserved.  


<a id="orgb29e273"></a>

### Changes in other utilities does not affect R1 or R2

Details: <https://wiki.clusterlabs.org/wiki/Pacemaker_2.0_Tool_Changes#Other_changes>  


<a id="orge8ebad7"></a>

## The summary of changes between 1.1 and 2.0 versions relevant for R1, R2 releases:


<a id="orge980bc6"></a>

### Cluster objects attributes renamed

Affects scripts that create/maintain cluster.  


<a id="org428b19c"></a>

### Tool changes

May affect userguides and script that analyze log files output  


<a id="orgeaafc00"></a>

### CIB XML

May affect scripts that work somehow with CIB XML output. Low probability.  


<a id="org923991a"></a>

### Deprecated syntax can't be used since support will be dropped after some 2.0.X release
