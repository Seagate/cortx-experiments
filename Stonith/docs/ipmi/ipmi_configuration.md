
## Enable stonith property
  ```bash
    pcs property set no-quorum-policy=ignore
    pcs property set stonith-action=off
    pcs property set stonith-enabled=True
  ```

## Create IPMI Resource
  - For stonith-c1 update `<srvnode-1_bmc_ip>`, `<bmc_user>`, `<bmc_pass>`.
  ```bash
    pcs stonith create stonith-c1 fence_ipmilan ipaddr=<srvnode-1_bmc_ip> login=<bmc_user> passwd=<bmc_pass> delay=5 pcmk_host_list=srvnode-1 pcmk_host_check=static-list lanplus=true auth=PASSWORD power_timeout=40 verbose=true op monitor interval=10s meta failure-timeout=15s

    pcs stonith create stonith-c2 fence_ipmilan ipaddr=<srvnode-2_bmc_ip> login=<bmc_user> passwd=<bmc_pass> pcmk_host_list=srvnode-2 pcmk_host_check=static-list lanplus=true auth=PASSWORD power_timeout=40 verbose=true op monitor interval=10s meta failure-timeout=15s

    pcs constraint location stonith-c1 avoids srvnode-1
    pcs constraint location stonith-c2 avoids srvnode-2
  ```

## Update IPMI resource
  ```bash
    pcs stonith update stonith-c1 ipaddr=<srvnode-1_bmc_ip> login=<bmc_user> passwd=<bmc_pass>
    pcs stonith update stonith-c2 ipaddr=<srvnode-2_bmc_ip> login=<bmc_user> passwd=<bmc_pass>
  ```

## Delete IPMI resource agent
  ```bash
    pcs stonith delete stonith-c1
    pcs stonith delete stonith-c2
  ```
