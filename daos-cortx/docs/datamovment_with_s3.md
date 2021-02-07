# Daos object movement using aws s3cli

- Daos source container to Daos destination container object movement is possible using aws s3 cli. This documents is the setup guide to perform mentioned exercise.

# Test setup

## Prerequisites

* Single node deployment of cortx on another VM

    - The single node deployment for CORTX will hosting s3 server, which will be used to manage buckets and store objects requested aws s3 cli on daos node.

* Daos server node setup on a VM
  
    - Daos node will be required to create pools, containers and storing objects in it.

* Install s3 cli on Daos node

    - aws s3 cli Daos node will be used to storing/retrieving objects to/from CORTX node.
    
## Setup cortx node

  - Follow this [document](https://github.com/Seagate/cortx/blob/main/QUICK_START.md) to setup cortx on your vm.

  - Verify the installation using hctl status.

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

## Setup Daos node

- Follow this [document](https://github.com/Seagate/cortx-experiments/blob/main/daos-cortx/docs/setup_daos.md) to setup daos and creating container.
  
- Make sure CORTX and Daos node can communicate or both are in the same network. Try pinging cortx from daos or vice-versa to check connectivity.

## Install s3 cli on Daos node.

* Follow this [steps](https://github.com/Seagate/cortx-s3server/blob/main/docs/CORTX-S3%20Server%20Quick%20Start%20Guide.md#14-test-your-build-using-s3-cli) for installing s3 cli on daos node. 
 
* Add credentials on Daos node

      [root@ssc-vm-2162 ~]# cd ~/.aws/
      [root@ssc-vm-2162 ~]# ls
      config  credentials

- If these files are not already present then create them and populate both files with the same contents of credentials and config file on cortx node(residing at ~/.aws/).

- cortx node might be having following contents as below.

      [root@ssc-vm-2161 .aws]# cat config
      [default]
      output = text
      region = US
      s3 =
          endpoint_url = http://s3.seagate.com
      s3api =
          endpoint_url = http://s3.seagate.com
      ca_bundle = /etc/ssl/stx-s3-clients/s3/ca.crt

      [plugins]
      endpoint = awscli_plugin_endpoint
      [root@ssc-vm-2161 .aws]#
      [root@ssc-vm-2161 .aws]# cat credentials
      [default]
      aws_access_key_id = AKIAqQWHc###################
      aws_secret_access_key=  G6lFDsuvebBoOTfiKh###################

- Note : credentials are hidden above using pound sign.

- go to cortx node

        ls ~/.aws/credentials file`

        config credentials

- Copy contents from here and populate credentials and config files on daos node

* Register domain name on daos node.

- Added cortx node IP (s3.seagate.com) to /etc/hosts

* Create 2 containers inside a pool and mount using dfuse at following location

      /mnt/dfuse_data/src_container/
      /mnt/dfuse_data/dest_container/

* Create test object (a file) with some contents in source container's dfuse directory (i.e. inside /mnt/dfuse_data/src_container/)

`touch file_obj`

- Add some dummy contents inside this file.

* Create test-bucket on cortx node using following command

`[root@ssc-vm-2162 src_container]# aws s3 mb s3://daos-bucket`

* Verify bucket list on daos node

`[root@ssc-vm-2162 src_container]# aws s3 ls`

* Copy file_obj from /mnt/dfuse_data/src_container/ (i.e. container's dfuse mount point) to s3 bucket

`[root@ssc-vm-2162 src_container]# aws s3 cp file_obj s3://daos-bucket/`

- contents can be verified using `aws s3 ls s3://daos-bucket/` command.

* Copy back file to dest_container from s3 bucket

`cd /mnt/dfuse_data/dest_container/`

- Check contents

        [root@ssc-vm-2162 dest_container]# ls
        [root@ssc-vm-2162 dest_container]# 
 
 Currently directory would be empty.
 
 - Now copy contents from s3 bucket to dest_container

`[root@ssc-vm-2162 dest_container]# aws s3 cp s3://daos-bucket/file_obj .`

* Verified file contents inside dest_container

        [root@ssc-vm-2162 dest_container]# ls
        file_obj

Just like cp, one can also perform mv, sync, etc. operations.
