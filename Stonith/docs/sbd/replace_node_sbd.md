
## Remove Node

1. Remove node
  ```bash
    cortxha cluster remove_node srvnode-2
  ```

2. Disable SBD
  - We need to restart cluster if plan to add SBD
  ```bash
    pcs stonith sbd disable
      ```Output
        Disabling SBD service...
        srvnode-1: sbd disabled
        Warning: Cluster restart is required in order to apply these changes.
      ```
  ```

3. Add node
  ```bash
    cortxha cluster add_node srvnode-2
  ```

4. Stop cluster
  ```bash
    pcs cluster stop --all
      ```Output
        srvnode-1: Stopping Cluster (pacemaker)...
        srvnode-2: Stopping Cluster (pacemaker)...
        srvnode-1: Stopping Cluster (corosync)...
        srvnode-2: Stopping Cluster (corosync)...
      ```
  ```

5. Enable sbd on All node
  ```bash
    systemctl enable sbd
  ```

6. Start Cluster
  ```bash
    pcs cluster start --all
      ```Output
        srvnode-1: Starting Cluster (corosync)...
        srvnode-2: Starting Cluster (corosync)...
        srvnode-1: Starting Cluster (pacemaker)...
        srvnode-2: Starting Cluster (pacemaker)...
      ```
  ```
