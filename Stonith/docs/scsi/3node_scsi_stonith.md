# Setup on 3 VM's (Self fencing)

1. Did pcs cluster setup on below 3 nodes by following the documents: 
(https://github.com/Seagate/cortx-ha/wiki/Corosync-Pacemaker-Setup)

### Cluster details:
```
10.230.242.67  node1
10.230.242.95  node3
10.230.249.166  node2
```
### pcsd status (on all nodes):
```
-bash-4.2$ sudo pcs cluster status
[sudo] password for 730727:
Cluster Status:
 Stack: corosync
 Current DC: node2 (version 1.1.23-1.el7-9acf116022) - partition with quorum
 Last updated: Thu Jan  7 22:30:53 2021
 Last change: Thu Jan  7 03:01:36 2021 by root via cibadmin on node1
 3 nodes configured
 1 resource instance configured

PCSD Status:
  node2: Online
  node1: Online
  node3: Online
```

2. Created shared disk using iscsi server:

- Created new VM and configured the icsci server to use the shared virtual disk
- Followed below steps no iscsi server:

### Create Volume
```
-bash-4.2$ lsblk
NAME                         MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                            8:0    0   50G  0 disk
├─sda1                         8:1    0    1G  0 part /boot
└─sda2                         8:2    0   49G  0 part
  ├─vg_sysvol-lv_root        253:0    0   20G  0 lvm  /
  ├─vg_sysvol-lv_swap        253:1    0    1G  0 lvm  [SWAP]
  ├─vg_sysvol-lv_var         253:2    0   10G  0 lvm  /var
  ├─vg_sysvol-lv_log         253:3    0    8G  0 lvm  /var/log
  ├─vg_sysvol-lv_audit       253:4    0  256M  0 lvm  /var/log/audit
  └─vg_sysvol-lv_tmp         253:5    0    1G  0 lvm  /tmp
sdb                            8:16   0   25G  0 disk
sdc                            8:32   0   25G  0 disk
sr0                           11:0    1 1024M  0 rom
sr1                           11:1    1  374K  0 rom

-bash-4.2$ fdisk /dev/sdb
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x4eac8b9e.

Command (m for help): p

Disk /dev/vda: 53.7 GB, 53687091200 bytes, 104857600 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x4eac8b9e

   Device Boot      Start         End      Blocks   Id  System

Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-104857599, default 2048):
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-104857599, default 104857599):
Using default value 104857599
Partition 1 of type Linux and of size 50 GiB is set

Command (m for help): p

Disk /dev/vda: 53.7 GB, 53687091200 bytes, 104857600 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x4eac8b9e

   Device Boot      Start         End      Blocks   Id  System
/dev/vda1            2048   104857599    52427776   83  Linux

Command (m for help): t
Selected partition 1
Hex code (type L to list all codes): 8e
Changed type of partition 'Linux' to 'Linux LVM'

Command (m for help): p

Disk /dev/vda: 53.7 GB, 53687091200 bytes, 104857600 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x4eac8b9e

   Device Boot      Start         End      Blocks   Id  System
/dev/vda1            2048   104857599    52427776   8e  Linux LVM

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

### Check the volume created
```
-bash-4.2$ lsblk
NAME                         MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                            8:0    0   50G  0 disk
├─sda1                         8:1    0    1G  0 part /boot
└─sda2                         8:2    0   49G  0 part
  ├─vg_sysvol-lv_root        253:0    0   20G  0 lvm  /
  ├─vg_sysvol-lv_swap        253:1    0    1G  0 lvm  [SWAP]
  ├─vg_sysvol-lv_var         253:2    0   10G  0 lvm  /var
  ├─vg_sysvol-lv_log         253:3    0    8G  0 lvm  /var/log
  ├─vg_sysvol-lv_audit       253:4    0  256M  0 lvm  /var/log/audit
  └─vg_sysvol-lv_tmp         253:5    0    1G  0 lvm  /tmp
sdb                            8:16   0   25G  0 disk
└─sdb1                         8:17   0   25G  0 part
sdc                            8:32   0   25G  0 disk
sr0                           11:0    1 1024M  0 rom
sr1                           11:1    1  374K  0 rom
```

### Create PV
```
-bash-4.2$ pvcreate /dev/sdb1
  Physical volume "/dev/vda1" successfully created.

-------------------------------------------------------------
-bash-4.2$ vgcreate cluster_vg /dev/sdb1
  Volume group "cluster_vg" successfully created

-------------------------------------------------------------
-bash-4.2$ vgs
  VG         #PV #LV #SN Attr   VSize   VFree
  cluster_vg   1   0   0 wz--n- <50.00g <50.00g
  vg_sysvol    1   6   0 wz--n- <48.99g   4.00m

-------------------------------------------------------------
[root@ssc-vm-c-0087 708945]# lvcreate -L 1G cluster_vg -n cluster_disk1
  Logical volume "cluster_disk1" created.

-------------------------------------------------------------
[root@ssc-vm-c-0087 708945]# mkfs -t ext4 /dev/cluster_vg/cluster_disk1
mke2fs 1.42.9 (28-Dec-2013)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
65536 inodes, 262144 blocks
13107 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=268435456
8 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376

Allocating group tables: done
Writing inode tables: done
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done
```

### Check volume again
```
-bash-4.2$ lsblk
NAME                         MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                            8:0    0   50G  0 disk
├─sda1                         8:1    0    1G  0 part /boot
└─sda2                         8:2    0   49G  0 part
  ├─vg_sysvol-lv_root        253:0    0   20G  0 lvm  /
  ├─vg_sysvol-lv_swap        253:1    0    1G  0 lvm  [SWAP]
  ├─vg_sysvol-lv_var         253:2    0   10G  0 lvm  /var
  ├─vg_sysvol-lv_log         253:3    0    8G  0 lvm  /var/log
  ├─vg_sysvol-lv_audit       253:4    0  256M  0 lvm  /var/log/audit
  └─vg_sysvol-lv_tmp         253:5    0    1G  0 lvm  /tmp
sdb                            8:16   0   25G  0 disk
└─sdb1                         8:17   0   25G  0 part
  └─cluster_vg-cluster_disk1 253:6    0    1G  0 lvm
sdc                            8:32   0   25G  0 disk
sr0                           11:0    1 1024M  0 rom
sr1                           11:1    1  374K  0 rom
```

### Create iscsi storage (On iscsi node only)
```
-bash-4.2$ yum -y install targetcli

-bash-4.2$ targetcli
targetcli shell version 2.1.fb49
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.

/> backstores/block create disk1 /dev/cluster_vg/cluster_disk1
Created block storage object disk1 using /dev/cluster_vg/cluster_disk1.
/> iscsi/ create iqn.2021-06.com.lab:centos7
Created target iqn.2021-06.com.lab:centos7.
Created TPG 1.
Global pref auto_add_default_portal=true
Created default portal listening on all IPs (0.0.0.0), port 3260.
/> /iscsi/iqn.2021-06.com.lab:centos7/tpg1/portals/ create
Using default IP port 3260
Binding to INADDR_ANY (0.0.0.0)
This NetworkPortal already exists in configFS
/> iscsi/iqn.2021-06.com.lab:centos7/tpg1/luns create /backstores/block/disk1
Created LUN 0.
/> iscsi/iqn.2021-06.com.lab:centos7/tpg1/acls create iqn.2021-06.com.lab:node1
Created Node ACL for iqn.2021-06.com.lab:node1
Created mapped LUN 0.
/> iscsi/iqn.2021-06.com.lab:centos7/tpg1/acls create iqn.2021-06.com.lab:node2
Created Node ACL for iqn.2021-06.com.lab:node2
Created mapped LUN 0.
/> iscsi/iqn.2021-06.com.lab:centos7/tpg1/acls create iqn.2021-06.com.lab:node3
Created Node ACL for iqn.2021-06.com.lab:node3
Created mapped LUN 0.
/> exit
Global pref auto_save_on_exit=true
Configuration saved to /etc/target/saveconfig.json

---------------------------------------------------
-bash-4.2$ targetcli ls

o- / ......................................................................................................................... [...]
  o- backstores .............................................................................................................. [...]
  | o- block .................................................................................................. [Storage Objects: 1]
  | | o- disk1 ....................................................... [/dev/cluster_vg/cluster_disk1 (1.0GiB) write-thru activated]
  | |   o- alua ................................................................................................... [ALUA Groups: 1]
  | |     o- default_tg_pt_gp ....................................................................... [ALUA state: Active/optimized]
  | o- fileio ................................................................................................. [Storage Objects: 0]
  | o- pscsi .................................................................................................. [Storage Objects: 0]
  | o- ramdisk ................................................................................................ [Storage Objects: 0]
  o- iscsi ............................................................................................................ [Targets: 1]
  | o- iqn.2021-06.com.lab:centos7 ....................................................................................... [TPGs: 1]
  |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
  |     o- acls .......................................................................................................... [ACLs: 3]
  |     | o- iqn.2021-06.com.lab:node1 ............................................................................ [Mapped LUNs: 1]
  |     | | o- mapped_lun0 ................................................................................. [lun0 block/disk1 (rw)]
  |     | o- iqn.2021-06.com.lab:node2 ............................................................................ [Mapped LUNs: 1]
  |     | | o- mapped_lun0 ................................................................................. [lun0 block/disk1 (rw)]
  |     | o- iqn.2021-06.com.lab:node3 ............................................................................ [Mapped LUNs: 1]
  |     |   o- mapped_lun0 ................................................................................. [lun0 block/disk1 (rw)]
  |     o- luns .......................................................................................................... [LUNs: 1]
  |     | o- lun0 ................................................. [block/disk1 (/dev/cluster_vg/cluster_disk1) (default_tg_pt_gp)]
  |     o- portals .................................................................................................... [Portals: 1]
  |       o- 0.0.0.0:3260 ..................................................................................................... [OK]
  o- loopback ......................................................................................................... [Targets: 0]
---------------------------------------------------
```

### Create iscsi client on node1, node2 and node3
```
---------------------------------------------------
Login to node1
---------------------------------------------------
[root@node01 ~]# yum -y install iscsi-initiator-utils
[root@node01 ~]# vi /etc/iscsi/initiatorname.iscsi
# change to the same IQN you set on the iSCSI target server acl name
InitiatorName=iqn.2021-06.com.lab:node1
# save file
-bash-4.2$ sudo iscsiadm -m discovery -t sendtargets -p 10.230.250.178
10.230.250.178:3260,1 iqn.2021-06.com.lab:centos7
-bash-4.2$ sudo iscsiadm -m node --login
able to login successfully.

-------------------------------------------------------------
Login to node2
---------------------------------------------------
[root@node01 ~]# yum -y install iscsi-initiator-utils
[root@node01 ~]# vi /etc/iscsi/initiatorname.iscsi
# change to the same IQN you set on the iSCSI target server acl name
InitiatorName=iqn.2021-06.com.lab:node2
# save file
-bash-4.2$ sudo iscsiadm -m discovery -t sendtargets -p 10.230.250.178
10.230.250.178:3260,1 iqn.2021-06.com.lab:centos7
-bash-4.2$ sudo iscsiadm -m node --login
able to login successfully.

-------------------------------------------------------------
# Login to node3
---------------------------------------------------
[root@node01 ~]# yum -y install iscsi-initiator-utils
[root@node01 ~]# vi /etc/iscsi/initiatorname.iscsi
# change to the same IQN you set on the iSCSI target server acl name
InitiatorName=iqn.2021-06.com.lab:node3
# save file
-bash-4.2$ sudo iscsiadm -m discovery -t sendtargets -p 10.230.250.178
10.230.250.178:3260,1 iqn.2021-06.com.lab:centos7
-bash-4.2$ sudo iscsiadm -m node --login
able to login successfully.
*** Successfully able to create shared disk using iscsi server and cluster nodes as initiator's in the setup.
```

### On all nodes:
```
-bash-4.2$ iscsiadm -m session -o show
tcp: [1] 10.230.250.178:3260,1 iqn.2021-06.com.lab:centos7 (non-flash)
-------------------------------------------------------------
# Install fence-agents (All Nodes)
[root@ssc ]# yum install -y sbd fence-agents-all

    version:
        Installing:
        fence-agents-all           x86_64 4.2.1-30.el7_8.1
        sbd                        x86_64 1.4.0-15.el7
```

3. Configure stonith using iscsi shared disk for all nodes & enable it:
```
a. check reservation on all nodes

-bash-4.2$ sudo /usr/bin/sg_persist -n -i -k -d /dev/sdd
[sudo] password for 730727:
  PR generation=0x0, there are NO registered reservation keys
 
b. create stonith device

pcs stonith create scsi-shooter fence_scsi pcmk_host_list="node1 node2 node3" devices=/dev/sdd 
pcmk_monitor_action="metadata" pcmk_reboot_action="off" meta provides="unfencing"

c. again check reservation
-bash-4.2$  sudo /usr/bin/sg_persist -n -i -k -d /dev/sdb
  PR generation=0x2, 2 registered reservation keys follow:
    0x74ca0002
    0x74ca0000

d. Configure watchdog for scsi reservation. (All Node)

-bash-4.2$  yum install watchdog
# Soft reboot for fence_scsi
-bash-4.2$  cp /usr/share/cluster/fence_scsi_check.pl /etc/watchdog.d/

# Hard reboot for fence_scsi

-bash-4.2$  cp /usr/share/cluster/fence_scsi_check_hardreboot /etc/watchdog.d/
-bash-4.2$  chkconfig watchdog on
-bash-4.2$  service watchdog start

e. pcs cluster properties: (set properties if not present)
-bash-4.2$ sudo  pcs property
Cluster Properties:
 cluster-infrastructure: corosync
 cluster-name: amol_cluster
 dc-version: 1.1.23-1.el7-9acf116022
 stonith-enabled: True
```

5. Did fence testing 
```
1. Bring down one node by closing the network using iptables cmds.

Bring down node 10.230.242.95 (node3)
ip link set down eth0
```

6. See the results
```
on node1 and node2:

-bash-4.2$ sudo pcs cluster  status
[sudo] password for 730727:
Cluster Status:
 Stack: corosync
 Current DC: node2 (version 1.1.23-1.el7-9acf116022) - partition with quorum
 Last updated: Thu Jan  7 23:50:23 2021
 Last change: Thu Jan  7 03:01:36 2021 by root via cibadmin on node1
 3 nodes configured
 1 resource instance configured

PCSD Status:
  node2: Online
  node1: Online
  node3: Offline

On node3:

-bash-4.2$ sudo pcs cluster status
[sudo] password for 730727:
Cluster Status:
 Stack: corosync
 Current DC: node2 (version 1.1.23-1.el7-9acf116022) - partition with quorum
 Last updated: Thu Jan  7 22:35:38 2021
 Last change: Thu Jan  7 03:01:36 2021 by root via cibadmin on node1
 3 nodes configured
 1 resource instance configured

PCSD Status:
  node3: Online

# Note: It just hanged here and putty session became inactive. Means the node is rebooted somehow.
# After 30/40 seconds node rebooted succesfully & joined cluster again.

on all nodes

-bash-4.2$ sudo pcs cluster  status
[sudo] password for 730727:
Cluster Status:
 Stack: corosync
 Current DC: node2 (version 1.1.23-1.el7-9acf116022) - partition with quorum
 Last updated: Thu Jan  7 23:50:23 2021
 Last change: Thu Jan  7 03:01:36 2021 by root via cibadmin on node1
 3 nodes configured
 1 resource instance configured

PCSD Status:
  node2: Online
  node1: Online
  node3: Online
```

