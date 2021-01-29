# Scsi configuration on target

### Create Volume

```
-------------------------------------------------------------
[root@ssc-vm-c-0087 User]# lsblk
NAME                   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                      8:0    0   50G  0 disk
├─sda1                   8:1    0    1G  0 part /boot
└─sda2                   8:2    0   49G  0 part
  ├─vg_sysvol-lv_root  253:0    0 25.4G  0 lvm  /
  ├─vg_sysvol-lv_swap  253:1    0    1G  0 lvm  [SWAP]
  ├─vg_sysvol-lv_tmp   253:2    0    1G  0 lvm  /tmp
  ├─vg_sysvol-lv_audit 253:3    0  256M  0 lvm  /var/log/audit
  ├─vg_sysvol-lv_log   253:4    0  9.3G  0 lvm  /var/log
  └─vg_sysvol-lv_var   253:5    0   12G  0 lvm  /var
sr0                     11:0    1  4.2G  0 rom
vda                    252:0    0   50G  0 disk
vdb                    252:16   0   50G  0 disk

-------------------------------------------------------------
[root@ssc-vm-c-0087 User]# fdisk /dev/vda
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

-------------------------------------------------------------
[root@ssc-vm-c-0087 User]# lsblk
NAME                   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                      8:0    0   50G  0 disk
├─sda1                   8:1    0    1G  0 part /boot
└─sda2                   8:2    0   49G  0 part
  ├─vg_sysvol-lv_root  253:0    0 25.4G  0 lvm  /
  ├─vg_sysvol-lv_swap  253:1    0    1G  0 lvm  [SWAP]
  ├─vg_sysvol-lv_tmp   253:2    0    1G  0 lvm  /tmp
  ├─vg_sysvol-lv_audit 253:3    0  256M  0 lvm  /var/log/audit
  ├─vg_sysvol-lv_log   253:4    0  9.3G  0 lvm  /var/log
  └─vg_sysvol-lv_var   253:5    0   12G  0 lvm  /var
sr0                     11:0    1  4.2G  0 rom
vda                    252:0    0   50G  0 disk
└─vda1                 252:1    0   50G  0 part
vdb                    252:16   0   50G  0 disk

-------------------------------------------------------------
[root@ssc-vm-c-0087 User]# pvcreate /dev/vda1
  Physical volume "/dev/vda1" successfully created.

-------------------------------------------------------------
[root@ssc-vm-c-0087 User]# vgcreate cluster_vg /dev/vda1
  Volume group "cluster_vg" successfully created

-------------------------------------------------------------
[root@ssc-vm-c-0087 User]# vgs
  VG         #PV #LV #SN Attr   VSize   VFree
  cluster_vg   1   0   0 wz--n- <50.00g <50.00g
  vg_sysvol    1   6   0 wz--n- <48.99g   4.00m

-------------------------------------------------------------
[root@ssc-vm-c-0087 User]# lvcreate -L 1G cluster_vg -n cluster_disk1
  Logical volume "cluster_disk1" created.

-------------------------------------------------------------
[root@ssc-vm-c-0087 User]# mkfs -t ext4 /dev/cluster_vg/cluster_disk1
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

### Create Scsi storage
```

[root@dlp ~]# yum -y install targetcli

[root@ssc-vm-c-0087 User]# targetcli
targetcli shell version 2.1.fb49
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.

/> backstores/block create disk1 /dev/cluster_vg/cluster_disk1
Created block storage object disk1 using /dev/cluster_vg/cluster_disk1.
/> iscsi/ create iqn.2015-06.com.lab:rhel7
Created target iqn.2015-06.com.lab:rhel7.
Created TPG 1.
Global pref auto_add_default_portal=true
Created default portal listening on all IPs (0.0.0.0), port 3260.
/> /iscsi/iqn.2015-06.com.lab:rhel7/tpg1/portals/ create
Using default IP port 3260
Binding to INADDR_ANY (0.0.0.0)
This NetworkPortal already exists in configFS
/> iscsi/iqn.2015-06.com.lab:rhel7/tpg1/luns create /backstores/block/disk1
Created LUN 0.
/> iscsi/iqn.2015-06.com.lab:rhel7/tpg1/acls create iqn.2015-06.com.lab:sevnode-1
Created Node ACL for iqn.2015-06.com.lab:sevnode-1
Created mapped LUN 0.
/> iscsi/iqn.2015-06.com.lab:rhel7/tpg1/acls create iqn.2015-06.com.lab:sevnode-2
Created Node ACL for iqn.2015-06.com.lab:sevnode-2
Created mapped LUN 0.
/> exit
Global pref auto_save_on_exit=true
Configuration saved to /etc/target/saveconfig.json

---------------------------------------------------
[root@ssc-vm-c-0087 User]# targetcli ls
o- / ................................................................................ [...]
  o- backstores ..................................................................... [...]
  | o- block ......................................................... [Storage Objects: 1]
  | | o- disk1 .............. [/dev/cluster_vg/cluster_disk1 (1.0GiB) write-thru activated]
  | |   o- alua .......................................................... [ALUA Groups: 1]
  | |     o- default_tg_pt_gp .............................. [ALUA state: Active/optimized]
  | o- fileio ........................................................ [Storage Objects: 0]
  | o- pscsi ......................................................... [Storage Objects: 0]
  | o- ramdisk ....................................................... [Storage Objects: 0]
  o- iscsi ................................................................... [Targets: 1]
  | o- iqn.2015-06.com.lab:rhel7 ................................................ [TPGs: 1]
  |   o- tpg1 ...................................................... [no-gen-acls, no-auth]
  |     o- acls ................................................................. [ACLs: 2]
  |     | o- iqn.2015-06.com.lab:sevnode-1 ............................... [Mapped LUNs: 1]
  |     | | o- mapped_lun0 ........................................ [lun0 block/disk1 (rw)]
  |     | o- iqn.2015-06.com.lab:sevnode-2 ............................... [Mapped LUNs: 1]
  |     |   o- mapped_lun0 ........................................ [lun0 block/disk1 (rw)]
  |     o- luns ................................................................. [LUNs: 1]
  |     | o- lun0 ........ [block/disk1 (/dev/cluster_vg/cluster_disk1) (default_tg_pt_gp)]
  |     o- portals ........................................................... [Portals: 1]
  |       o- 0.0.0.0:3260 ............................................................ [OK]
  o- loopback ................................................................ [Targets: 0]
```


# Scsi configuration on client

### Login scsi
```
[root@node01 ~]# yum -y install iscsi-initiator-utils

-------------------------------------------------------------
[root@node01 ~]# vi /etc/iscsi/initiatorname.iscsi
# change to the same IQN you set on the iSCSI target server
InitiatorName=iqn.2019-10.world.srv:node01.initiator01

-------------------------------------------------------------
[root@node01 ~]# vi /etc/iscsi/iscsid.conf
# line 58: uncomment
node.session.auth.authmethod = CHAP
# line 62,63: uncomment and specify the username and password you set on the iSCSI target server
node.session.auth.username = username
node.session.auth.password = password
# discover target

-------------------------------------------------------------
[root@node01 ~]# iscsiadm -m discovery -t sendtargets -p 10.0.0.30
[  410.458613] Loading iSCSI transport class v2.0-870.
[  410.498521] iscsi: registered transport (tcp)
10.0.0.30:3260,1 iqn.2019-10.world.srv:dlp.target01

# confirm status after discovery

-------------------------------------------------------------
[root@node01 ~]# iscsiadm -m node -o show
# BEGIN RECORD 2.0-876
node.name = iqn.2019-10.world.srv:dlp.target01
node.tpgt = 1
node.startup = automatic
node.leading_login = No
iface.iscsi_ifacename = default
.....
.....
node.conn[0].iscsi.IFMarker = No
node.conn[0].iscsi.OFMarker = No
# END RECORD

# login to the target

-------------------------------------------------------------
[root@node01 ~]# iscsiadm -m node --login
Logging in to [iface: default, target: iqn.2019-10.world.srv:dlp.target01, portal: 10.0.0.30,3260] (multiple)
Login to [iface: default, target: iqn.2019-10.world.srv:dlp.target01, portal: 10.0.0.30,3260] successful.

# confirm the established session

-------------------------------------------------------------
[root@node01 ~]# iscsiadm -m session -o show
tcp: [1] 10.0.0.30:3260,1 iqn.2019-10.world.srv:dlp.target01 (non-flash)
# confirm the partitions

-------------------------------------------------------------
[root@node01 ~]# cat /proc/partitions
major minor  #blocks  name

 252        0   31457280 sda
 252        1    1048576 sda1
 252        2   30407680 sda2
 253        0   15728640 dm-0
 253        1    3145728 dm-1
   8        0   10485760 sdb
# added new device provided from the target server as [sdb]
```

# Configure multipart on client
```
[root@node01 ~]# yum -y install iscsi-initiator-utils

-------------------------------------------------------------
[root@node01 ~]# vi /etc/iscsi/initiatorname.iscsi
# change to the same IQN you set on the iSCSI target server
InitiatorName=iqn.2019-10.world.srv:node01.initiator01

-------------------------------------------------------------

[root@ssc-vm-c-1628 User]# iscsiadm -m discovery -t sendtargets -p 10.230.240.183
10.230.240.183:3260,1 iqn.2015-06.com.lab:rhel7
[root@ssc-vm-c-1628 User]# iscsiadm -m discovery -t sendtargets -p 192.168.13.224
192.168.13.224:3260,1 iqn.2015-06.com.lab:rhel7
[root@ssc-vm-c-1628 User]# iscsiadm -m discovery -t sendtargets -p 192.168.30.222
192.168.30.222:3260,1 iqn.2015-06.com.lab:rhel7

-------------------------------------------------------------

# login to the target
[root@node01 ~]# iscsiadm -m node --login
Logging in to [iface: default, target: iqn.2019-10.world.srv:dlp.target01, portal: 10.0.0.30,3260] (multiple)
Login to [iface: default, target: iqn.2019-10.world.srv:dlp.target01, portal: 10.0.0.30,3260] successful.

[root@ssc-vm-c-1628 User]# yum install device-mapper-multipath -y

[root@ssc-vm-c-1628 User]# systemctl start multipathd.service

[root@ssc-vm-c-1628 User]# multipath -ll
Dec 04 01:40:13 | DM multipath kernel driver not loaded
Dec 04 01:40:13 | /etc/multipath.conf does not exist, blacklisting all devices.
Dec 04 01:40:13 | A default multipath.conf file is located at
Dec 04 01:40:13 | /usr/share/doc/device-mapper-multipath-0.4.9/multipath.conf
Dec 04 01:40:13 | You can run /sbin/mpathconf --enable to create
Dec 04 01:40:13 | /etc/multipath.conf. See man mpathconf(8) for more details
Dec 04 01:40:13 | DM multipath kernel driver not loaded

[root@ssc-vm-c-1629 User]#  mpathconf --user_friendly_names n

[root@ssc-vm-c-1628 User]# systemctl restart multipathd.service

[root@ssc-vm-c-1628 User]# multipath -ll
36001405d02283f6185849c995c65c903 dm-6 LIO-ORG ,disk1
size=1.0G features='0' hwhandler='0' wp=rw
|-+- policy='service-time 0' prio=1 status=active
| `- 3:0:0:0 sdc 8:32 active ready running
|-+- policy='service-time 0' prio=1 status=enabled
| `- 4:0:0:0 sdd 8:48 active ready running
`-+- policy='service-time 0' prio=1 status=enabled
  `- 5:0:0:0 sde 8:64 active ready running
[root@ssc-vm-c-1628 User]#

[root@ssc-vm-c-1628 User]# vim /etc/multipath.conf
defaults {
        polling_interval        10
        path_selector           "round-robin 0"
        path_grouping_policy    multibus
        uid_attribute           ID_SERIAL
        prio                    alua
        path_checker            readsector0
        rr_min_io               100
        max_fds                 8192
        rr_weight               priorities
        failback                immediate
        no_path_retry           fail
        user_friendly_names     yes
}

multipaths {
    multipath {
            wwid "36001405d02283f6185849c995c65c903" # wwid for a cluster-shared device
            alias "ha_data"
            reservation_key 0x1 # unique to this node - change for other nodes
    }
}

[root@ssc-vm-c-1628 User]# systemctl restart multipathd.service
[root@ssc-vm-c-1628 User]# lsblk
NAME                   MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                      8:0    0   50G  0 disk
sdb                      8:16   0   50G  0 disk
sdc                      8:32   0    1G  0 disk
└─ha_data              253:6    0    1G  0 mpath
sdd                      8:48   0    1G  0 disk
└─ha_data              253:6    0    1G  0 mpath
sde                      8:64   0    1G  0 disk
└─ha_data              253:6    0    1G  0 mpath
sr0                     11:0    1 1024M  0 rom
sr1                     11:1    1  374K  0 rom
vda                    252:0    0   50G  0 disk
├─vda1                 252:1    0    1G  0 part  /boot
└─vda2                 252:2    0   49G  0 part
  ├─vg_sysvol-lv_root  253:0    0   25G  0 lvm   /
  ├─vg_sysvol-swap     253:1    0  764M  0 lvm   [SWAP]
  ├─vg_sysvol-lv_var   253:2    0   12G  0 lvm   /var
  ├─vg_sysvol-lv_log   253:3    0   10G  0 lvm   /var/log
  ├─vg_sysvol-lv_audit 253:4    0  256M  0 lvm   /var/log/audit
  └─vg_sysvol-lv_tmp   253:5    0    1G  0 lvm   /tmp


[root@ssc-vm-c-1629 User]# ls /dev/disk/by-id/dm-name-ha_data
/dev/disk/by-id/dm-name-ha_data

```

# Destroy


### Remove target multipath from client

```
# Remove multipath device
multipath -f

# logout scsi
iscsiadm --mode node --logoutall=all

# Check descovery for scsi
iscsiadm -m discoverydb

# Remove for each descovery
iscsiadm -m discoverydb -o delete -p ip:port -t type

# Remove rpm
yum remove -y iscsi-initiator-utils
```

### Remove iqn and lun from server
```
targetcli /iscsi delete iqn.2003-01.org.linux-iscsi.node1.x8664:sn.2613f8620d98
targetcli /backstores/block delete storage1
targetcli ls
targetctl save
rm -rf /etc/systemd/system/fjsvsdx.service.d/
systemctl daemon-reload
systemctl disable target.service
systemctl stop target.service
```
