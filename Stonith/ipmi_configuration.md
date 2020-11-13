
## Enable stonith property
  ```bash
    pcs property set no-quorum-policy=ignore
    pcs property set stonith-action=off
    pcs property set stonith-enabled=True
  ```

## Create IPMI Resource
  ```
    pcs stonith create stonith-c1 fence_ipmilan auth=PASSWORD ipaddr=<srvnode-1_bmc_ip> lanplus=true login=<bmc_user> passwd=<bmc_pass> pcmk_host_check=static-list pcmk_host_list=srvnode-1 power_timeout=40

    pcs stonith create stonith-c2 fence_ipmilan auth=PASSWORD ipaddr=<srvnode-1_bmc_ip> lanplus=true login=<bmc_user> passwd=<bmc_pass> pcmk_host_check=static-list pcmk_host_list=srvnode-2 power_timeout=40

    pcs constraint location stonith-c1 avoids srvnode-1
    pcs constraint location stonith-c2 avoids srvnode-2
  ```