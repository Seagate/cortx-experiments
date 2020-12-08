# Configure scsi_fence assuming shared volume available

1. Install fence-agents (All Nodes)
  ```
  [root@ssc ]# yum install -y sbd fence-agents-all

      version:
          Installing:
          fence-agents-all           x86_64 4.2.1-30.el7_8.1
          sbd                        x86_64 1.4.0-15.el7
  ```

2. Check Persistance Reservation (All Node)
  ```
  [root@ssc ]# /usr/bin/sg_persist -n -i -k -d /dev/disk/by-id/dm-name-ha_data
    PR generation=0x0, there are NO registered reservation keys
  ```

3. Configure scsi fencing agent (Single node)
  - Provided two way fence_scsi and fence_mpath. Select one of given fencing.
  - Device /dev/disk/by-id/dm-name-ha_data.
  - pcmk_host_list has list of host to be monitor by this agent.
  - `provides="unfencing"` allow pacemaker to treat other node unfencing and add to cluster after reboot.

  ```
  [root@ssc ]# pcs stonith create scsi-shooter fence_scsi pcmk_host_list="srvnode-1 srvnode-2" devices=/dev/disk/by-id/dm-name-ha_data pcmk_monitor_action="metadata" pcmk_reboot_action="off" meta provides="unfencing"

  # There are two keys c1b0000 for node1 and c1b0001 for node2
  [root@ssc ]# /usr/bin/sg_persist -n -i -k -d /dev/disk/by-id/dm-name-ha_data
    PR generation=0x6, 6 registered reservation keys follow:
      0xc1b0000
      0xc1b0001
      0xc1b0000
      0xc1b0001
      0xc1b0000
      0xc1b0001

  ################################### OR ############################################

  # Note: fence_mpath has no location constraint as each resource
    need to create key for each node.

  # Configure fence_mpath device
  [root@ssc ]# pcs stonith create mpath1 fence_mpath pcmk_on_timeout="70" pcmk_off_timeout="70" pcmk_host_list="srvnode-1" pcmk_monitor_action="metadata" pcmk_reboot_action="off" key=123abc devices="/dev/disk/by-id/dm-name-ha_data" power_wait="65" meta provides="unfencing"

  [root@ssc ]# pcs stonith create mpath2 fence_mpath pcmk_on_timeout="70" pcmk_off_timeout="70" pcmk_host_list="srvnode-2" pcmk_monitor_action="metadata" pcmk_reboot_action="off" key=456abc devices="/dev/disk/by-id/dm-name-ha_data" power_wait="65" meta provides="unfencing"

  ```

4. Configure watchdog for scsi reservation. (All Node)

  ```
  [root@ssc ]# yum install watchdog

  # Select one of them hard or soft reboot

  # Soft reboot for fence_scsi
  [root@ssc ]# cp /usr/share/cluster/fence_scsi_check.pl /etc/watchdog.d/

  # Hard reboot for fence_scsi
  [root@ssc ]# cp /usr/share/cluster/fence_scsi_check_hardreboot /etc/watchdog.d/

  # Soft reboot for fence_mpath
  [root@ssc ]# cp /usr/share/cluster/fence_mpath_check /etc/watchdog.d/

  # Hard reboot for fence_mpath
  [root@ssc ]# cp /usr/share/cluster/fence_mpath_check_hardreboot /etc/watchdog.d/

  [root@ssc ]# chkconfig watchdog on
  [root@ssc ]# service watchdog start
	
  ```

## fence_scsi vs fence_mpath

  - Both fence_scsi and fence_mpath have same result but reservation is different.
  - fence_scsi if used with multipart device then it create multiple dublicate key for each pointing device of multipart.
  - fence_mpath create single key for one multipart device.
  - Example:
```
[root@ssc]# lsblk
NAME                   MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sdc                      8:32   0    1G  0 disk
└─ha_data              253:8    0    1G  0 mpath
sdd                      8:48   0    1G  0 disk
└─ha_data              253:8    0    1G  0 mpath
sde                      8:64   0    1G  0 disk
└─ha_data              253:8    0    1G  0 mpath

# Fence scsi reservation for each device pointed by multipart
  - 3 key for node1 and other 3 for node2
  - for device sdc, sdd, sde on node1 have c1b0000 and on node2 have c1b0001 key.

[root@ssc ]# /usr/bin/sg_persist -n -i -k -d /dev/disk/by-id/dm-name-ha_data
PR generation=0x6, 6 registered reservation keys follow:
  0xc1b0000
  0xc1b0001
  0xc1b0000
  0xc1b0001
  0xc1b0000
  0xc1b0001

# Fence mpath reservation for each device
  - For mpath we need to create resource for each node.
  - Registered each others key in the device
  - mpath1 has 123abc key for for each node.
  - mpath2 create 456abc key for each node.

[root@rh80-03 ~]# mpathpersist -i -k -d /dev/disk/by-id/dm-name-ha_data
  PR generation=0x10c,  4 registered reservation keys follow:
    0x123abc
    0x123abc
    0x456abc
    0x456abc
```

## Testing:
  - Bring down one of heartbeat network.

## Result:
  - After fencing, faulty node reservation key will be removed.
    - If faulty node still in connection then that node will be stopped in cluster.
    - If faulty node is not in cluster (split brain) then healthy node make faulty node offline and move all resource.
  - After key removed for faulty node watchdog will reboot node.
  - We can modify script to perform poweroff instead reboot

## Drawback:
  - Shutdown is not possible with watchdog we need to create external cronjob or
daemon to poweroff node.

