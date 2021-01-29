# Daos object movement using aws s3cli

- Daos source container to daos destination container object movement is possible using aws s3 cli. This setup demands following requisites.

## prerequisites

* Daos server setup on a VM 
  
    - Daos node will be required to create pools, contianers and storing objects in it. refer to <TODO>

* Install s3 cli on daos node

    - aws s3 cli daos node will be used to storing/retriving objects to/from cortx node. refer to <TODO>

* single node deployment of cortx

    - The single node deployment for CORTX will hosting s3 server, which will be used to manage buckets and store objects requested aws s3 cli on daos node. refer to <TODO>

# Steps :

* Setup CORTX node

 - Acquired a VM for cortx single node deployment. deployed it and verified the installation using hctl status.

        [root@ssc-vm-2161 ~]# hctl status

        Profile: 0x7000000000000001:0x1c

        Data pools:
        0x6f00000000000001:0x1d

        Services:
        srvnode-1 (RC)
        [started] hax 0x7200000000000001:0x6 192.168.29.186@tcp:12345:1:1
        [started] confd 0x7200000000000001:0x9 192.168.29.186@tcp:12345:2:1
        [started] ioservice 0x7200000000000001:0xc 192.168.29.186@tcp:12345:2:2
        [started] s3server 0x7200000000000001:0x16 192.168.29.186@tcp:12345:3:1
        [unknown] m0_client 0x7200000000000001:0x19 192.168.29.186@tcp:12345:4:1

* Setup daos node

- Quickstart <TODO>
  
- make sure cortx and daos node can communicate or both are in the same network. Try pinging cortx from daos or vice-versa to check connectivity.

* installed s3 cli on daos node.

- setup <TODO>

      [root@ssc-vm-2162 test_src]# aws s3 ls
      2021-01-24 10:31:58 daos-bucket
      [root@ssc-vm-2162 test_dest]#

* Added same credentials for access of cortx node inside ~/.aws/credentials file (after creating) on daos node.

* Register domain name on daos node.

- added cortx node IP (s3.seagate.com) to /etc/hosts

* Created 2 containers inside a pull and mount using dfuse at following location

      /mnt/dfuse_data/test_src/
      /mnt/dfuse_data/dest_src/

* created fileA inside with some contents in container's dfuse directory test_src //

* create test-bucket on cortx node using following command

`aws s3 mb s3://test-bucket`

* verified bucket list on daos node

`aws s3 ls`

* copied fileA from /mnt/dfuse_data/test_src/ (dfuse location) to s3 bucket

`aws s3 cp fileA s3://test-bucket/`

* copied back file to dest_src from s3 bucket.

`aws s3 cp s3://test-bucket/fileA .`

* verified file contents inside dest_src

Just like cp, one can also perform mv, sync, etc. operations.
