# Network Teaming

In this experiment, we would be focussing on achieving network teaming on data network (as management network teaming results in loss of connectivity to VM over ssh).  
Another aspect to consider here is the teaming has to be achieved using `ifcfg` network config files and **_not the nmcli commands_**.  

## Introduction

Network teaming is a method for linking NICs together logically to allow for failover or higher throughput.  
Teaming is a new implementation that does not affect the older bonding driver in the Linux kernel; it offers an alternate implementation. In earlier versions of RHEL, network bonding was the default method for creating aggregated network interfaces.  
  
In RHEL 7, network teaming has been added as a solution. The main difference between these two is that network bonding happened completely in kernel space using a special kernel module named bonding, whereas, in network teaming, the teamd daemon is added to allow interaction in user space as well.  
  
CentOS/RHEL 7 implements network teaming with a small kernel driver and a userspace daemon, teamd. The kernel handles network packets efﬁciently and teamd handles logic and interface processing. Software, called runners, implement load balancing and active-backup logic, such as roundrobin.  
  
CentOS/RHEL 7 supports channel bonding for backward compatibility. Network teaming provides better performance and is more extensible because of its modular design.   
Thus, even if both methods are still valid, network teaming is the preferred method.  

## Teamd Runners
The kernel takes care of handling network packets, while the teamd driver handles logic and interface processing. To determine how exactly this is happening, different runners are used. Runners in teaming are equivalent to the bonding modes. They are used to define the logic of traffic handling between the interfaces that are involved in the configuration. The table below gives a summary of available runners:  
Runner|Description
:--------|:---------------
**broadcast**| A simple runner which transmits each packet from all ports.
**roundrobin**| A simple runner which transmits packets in a round-robin fashion from each of the ports.
**activebackup**| This is a fail-over runner, which watches for link changes and selects an active port for data transfers.
**loadbalance**| This runner monitors trafﬁc and uses a hash function to try to reach a perfect balance when selecting ports for packet transmission.
**lacp**| This runner implements the 802.3ad Link Aggregation Control Protocol. Can use the same transmit port selection possibilities as the loadbalance runner.

## **Persistent Configuration**: Configure Network Team Using **ifcfg** Files
For scope of this experiment we want a configuration strategy that stays persistent across multiple system reboots, providing for consistent results every time.
For this we choose to use a method that involves modification of the ifcfg files under: `/etc/sysconfig/network-scripts`

### Procedure
1.  Go to the `/etc/sysconfig/network-scripts` directory and create **ifcfg-team0** file with below contents:
    ```
    DEVICE=team0
    DEVICETYPE=Team
    ONBOOT=yes
    BOOTPROTO=none
    IPADDR=172.10.10.11
    PREFIX=24
    TEAM_CONFIG='{"runner": {"name": "activebackup"}, "link_watch": {"name": "ethtool"}}'
    ```
    **NOTE**: You can copy the reference file `ifcfg-team0` under **_src_** to the target location: `/etc/sysconfig/network-scripts/ifcfg-team0`

1.  Edit the files for respective interface. In our case, **ifcfg-eth1** and **ifcfg-eth2**
    Reference file: `src/ifcfg-eth1`
    ```
    DEVICE=eth1
    DEVICETYPE=TeamPort
    ONBOOT=yes
    NM_CONTROLLED=no
    TEAM_MASTER=team0
    TEAM_PORT_CONFIG='{"prio": 100}'
    ```

    Reference file: `src/ifcfg-eth2`
    ```
    DEVICE=eth2
    DEVICETYPE=TeamPort
    ONBOOT=yes
    NM_CONTROLLED=no
    TEAM_MASTER=team0
    TEAM_PORT_CONFIG='{"prio": 100}'
    ```

1.  Make sure
    1.  NetworkManager service is running
    1.  The interfaces **eth1** and **eth2** are down.
        **NOTE**: `ifdown eth1` or `ifdown eth2` would not work as we have changed `ifcfg-eth1` and `ifcfg-eth2` files by now.  
    1.  Execute the following commands to bring down the links:
    ```
    # ip link set eth1 down
    # ip link set eth2 down
    ```

1.  Bring up the team interface
    ```
    # ifup team0
    ```

1.  Verify the teaming configuration with “ip addr”, “nmcli device status” and “teamdctl” commands
    ```
    # ip addr
      1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
      valid_lft forever preferred_lft forever
      inet6 ::1/128 scope host
      valid_lft forever preferred_lft forever
      2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
      link/ether 00:15:5d:e7:8e:b6 brd ff:ff:ff:ff:ff:ff
      inet 192.168.94.105/28 brd 192.168.94.111 scope global noprefixroute dynamic eth0
      valid_lft 86182sec preferred_lft 86182sec
      inet6 fe80::215:5dff:fee7:8eb6/64 scope link
      valid_lft forever preferred_lft forever
      3: eth1: <BROADCAST,MULTICAST> mtu 1500 qdisc mq state DOWN group default qlen 1000
      link/ether 00:15:5d:e7:8e:b7 brd ff:ff:ff:ff:ff:ff
      4: eth2: <BROADCAST,MULTICAST> mtu 1500 qdisc mq state DOWN group default qlen 1000
      link/ether 00:15:5d:e7:8e:b8 brd ff:ff:ff:ff:ff:ff
      5: team0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
      link/ether 96:20:31:4c:2c:7f brd ff:ff:ff:ff:ff:ff
      inet 172.16.0.11/24 brd 172.16.0.255 scope global team0
      valid_lft forever preferred_lft forever
    
    # nmcli device status
      DEVICE TYPE STATE CONNECTION
      eth0 ethernet connected System eth0
      eth1 ethernet unmanaged –
      eth2 ethernet unmanaged –
      lo loopback unmanaged –
      team0 team unmanaged –
    
    # teamdctl team0 state
      setup:
      runner: activebackup
      runner:
      active port:
    ```
Our Network teaming has been successfully been established over network interfaces, **eth1** and **eth2**.  

## What Didn't Work?
### SSC CloudForm VMs
SSC CloudForms VMs don't allow for a console access to any VM. Thus, if anything goes bad during the experiments, the entire VM is unreachable and there's no way to troubleshoot the attempt.  
To **workaround** this problem a CentOS 7.8 VM was setup on Windows Hyper-V using Vagrant.  


### Failed Attempt
An attempt to setup using the same steps as described above failed because the NetworkManager service was stopped.  
Before enabling teamd interface:  
```
    [root@srvnode-1 network-scripts]# ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
    valid_lft forever preferred_lft forever
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:e7:8e:b2 brd ff:ff:ff:ff:ff:ff
    inet 192.168.94.107/28 brd 192.168.94.111 scope global noprefixroute dynamic eth0
    valid_lft 86157sec preferred_lft 86157sec
    inet6 fe80::215:5dff:fee7:8eb2/64 scope link
    valid_lft forever preferred_lft forever
    3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:e7:8e:b4 brd ff:ff:ff:ff:ff:ff
    inet 172.19.10.11/16 brd 172.19.255.255 scope global noprefixroute eth1
    valid_lft forever preferred_lft forever
    inet6 fe80::215:5dff:fee7:8eb4/64 scope link
    valid_lft forever preferred_lft forever
    4: eth2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:e7:8e:b5 brd ff:ff:ff:ff:ff:ff
    inet 172.19.10.12/16 brd 172.19.255.255 scope global noprefixroute eth2
    valid_lft forever preferred_lft forever
    inet6 fe80::215:5dff:fee7:8eb5/64 scope link
    valid_lft forever preferred_lft forever
```

After enabling teamd interface:  
```
    [root@srvnode-1 network-scripts]# ifdown eth1
    INFO : [./ifdown-TeamPort] Team master is not present, skipping port device removal from master
    [root@srvnode-1 network-scripts]# ifdown eth2
    INFO : [./ifdown-TeamPort] Team master is not present, skipping port device removal from master
    [root@srvnode-1 network-scripts]# ifup team0
    does not seem to be present, delaying initialization.Device eth1
    does not seem to be present, delaying initialization.Device eth2
    does not seem to be present, delaying initialization.Device team0

    [root@srvnode-1 network-scripts]# ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
    valid_lft forever preferred_lft forever
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:e7:8e:b2 brd ff:ff:ff:ff:ff:ff
    inet 192.168.94.107/28 brd 192.168.94.111 scope global noprefixroute dynamic eth0
    valid_lft 86319sec preferred_lft 86319sec
    inet6 fe80::215:5dff:fee7:8eb2/64 scope link
    valid_lft forever preferred_lft forever
    3: eth1: <BROADCAST,MULTICAST> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether 00:15:5d:e7:8e:b4 brd ff:ff:ff:ff:ff:ff
    4: eth2: <BROADCAST,MULTICAST> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether 00:15:5d:e7:8e:b5 brd ff:ff:ff:ff:ff:ff
```
