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
  - Device /dev/disk/by-id/dm-name-ha_data
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
  ```

4. Configure watchdog for scsi reservation. (All Node)

  ```
  [root@ssc ]# yum install watchdog

  # Select one of them hard or soft reboot

  # For soft reboot
  [root@ssc ]# cp /usr/share/cluster/fence_scsi_check.pl /etc/watchdog.d/

  # For hard reboot
  [root@ssc ]# cp /usr/share/cluster/fence_scsi_check_hardreboot /etc/watchdog.d/

  [root@ssc ]# chkconfig watchdog on
  [root@ssc ]# service watchdog start

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

