# DAOS installation methods

There are three ways to install a daos server and client on your machine.
- RPM based
- DOCKER
- Source build method

Source based method is discussed below. Please note, that Provided commands are run as a root user.

# DAOS single-node server setup

Source based setup method: (follow -- https://daos-stack.github.io/admin/installation/#daos-from-scratch)

## Install dependencies (Specific to CentOS 7.8 / RHEL 7.7 )

    yum -y install epel-release; \
    yum -y install \
        boost-devel clang-analyzer cmake CUnit-devel doxygen file flex \
        gcc gcc-c++ git golang graphviz lcov                           \
        libaio-devel libcmocka-devel libevent-devel libiscsi-devel     \
        libtool libtool-ltdl-devel libuuid-devel libyaml-devel         \
        make meson nasm ninja-build numactl-devel openssl-devel        \
        pandoc patch python python-devel python36-devel python-magic   \
        python-pep8 python-pygit2 python2-pygithub python-requests     \
        readline-devel scons sg3_utils ShellCheck yasm pciutils        \
        valgrind-devel python36-pylint man java-1.8.0-openjdk maven    \
        json-c-devel python36-requests lz4-devel

    yum -y install \
           python2-avocado python2-avocado-plugins-output-html \
           python2-avocado-plugins-varianter-yaml-to-mux       \
           python-pathlib                                      \
           ndctl ipmctl e2fsprogs                              \
           python2-clustershell python2-Cython                 \
           python36-clustershell python36-paramiko             \
           python36-numpy python36-jira python3-pip Lmod       \
           fuse3-devel libipmctl-devel                         \
           hwloc-devel patchelf python36-tabulate              \
           java-1.8.0-openjdk python-distro python36-distro
    yum -y install openmpi3-devel

Use --skip-broken option if necessary.

## Clone repo

* For the current development version,

  ```git clone --recurse-submodules https://github.com/daos-stack/daos.git```
  
  - This is a master branch, which contains lates change. For object movment operation using mpifileutils one should use this source.

* To checkout the latest stable version,

  ```git clone --recurse-submodules -b v1.0.1 https://github.com/daos-stack/daos.git```
  
  - This contains recent TAG release and ensures stablity. latest tag can be found [here](https://daos-stack.github.io/admin/installation/#daos-source-code)
  
## Build daos

```cd daos```

```scons --config=force --build-deps=yes install```

    Terminal's ending logs --

    mpicc -o build/release/gcc/src/tests/simple_obj.o -c -Werror -g -Wshadow -Wall -Wno-missing-braces -fpic -D_GNU_SOURCE -DD_LOG_V2 -DDAOS_VERSION=\"1.1.2.1\" -DAPI_VERSION=\"0.9.0\" -DCMOCKA_FILTER_SUPPORTED=0 -DDAOS_BUILD_RELEASE -O2 -D_FORTIFY_SOURCE=2 -Wframe-larger-than=4096 -fno-strict-overflow -fno-delete-null-pointer-checks -fwrapv -fstack-protector-strong -fstack-clash-protection -DCART_VERSION=\"4.9.0\" -DDAOS_HAS_VALGRIND -Isrc/include/daos -Isrc/include -Isrc/cart/test/utest -Isrc/cart -Isrc/cart/include -Isrc/gurt -Iinstall/prereq/release/pmdk/include -Iinstall/prereq/release/isal/include -Iinstall/prereq/release/isal_crypto/include -Isrc/tests/suite -Iinstall/prereq/release/argobots/include -Iinstall/prereq/release/protobufc/include src/tests/simple_obj.c
    mpicc -o build/release/gcc/src/tests/simple_obj -Wl,-rpath-link=build/release/gcc/src/gurt -Wl,-rpath-link=build/release/gcc/src/cart -Wl,--enable-new-dtags -Wl,-rpath-link=/root/daos_src/daos/build/release/gcc/src/gurt -Wl,-rpath-link=/root/daos_src/daos/install/prereq/release/pmdk/lib -Wl,-rpath-link=/root/daos_src/daos/install/prereq/release/isal/lib -Wl,-rpath-link=/root/daos_src/daos/install/prereq/release/isal_crypto/lib -Wl,-rpath-link=/root/daos_src/daos/install/lib64/daos_srv -Wl,-rpath-link=/root/daos_src/daos/install/prereq/release/argobots/lib -Wl,-rpath-link=/root/daos_src/daos/install/prereq/release/protobufc/lib -Wl,-rpath-link=/root/daos_src/daos/install/lib64 -Wl,-rpath=/usr/lib -Wl,-rpath=\$ORIGIN/../../build/release/gcc/src/gurt -Wl,-rpath=\$ORIGIN/../prereq/release/pmdk/lib -Wl,-rpath=\$ORIGIN/../prereq/release/isal/lib -Wl,-rpath=\$ORIGIN/../prereq/release/isal_crypto/lib -Wl,-rpath=\$ORIGIN/../lib64/daos_srv -Wl,-rpath=\$ORIGIN/../prereq/release/argobots/lib -Wl,-rpath=\$ORIGIN/../prereq/release/protobufc/lib -Wl,-rpath=\$ORIGIN/../lib64 build/release/gcc/src/tests/simple_obj.o -Lbuild/release/gcc/src/gurt -Lbuild/release/gcc/src/cart/swim -Lbuild/release/gcc/src/cart -Lbuild/release/gcc/src/common -Linstall/prereq/release/pmdk/lib -Linstall/prereq/release/isal/lib -Linstall/prereq/release/isal_crypto/lib -Lbuild/release/gcc/src/bio -Lbuild/release/gcc/src/bio/smd -Lbuild/release/gcc/src/vea -Lbuild/release/gcc/src/vos -Lbuild/release/gcc/src/mgmt -Lbuild/release/gcc/src/pool -Lbuild/release/gcc/src/container -Lbuild/release/gcc/src/placement -Lbuild/release/gcc/src/dtx -Lbuild/release/gcc/src/object -Lbuild/release/gcc/src/rebuild -Lbuild/release/gcc/src/security -Lbuild/release/gcc/src/client/api -Lbuild/release/gcc/src/control -Linstall/prereq/release/argobots/lib -Linstall/prereq/release/protobufc/lib -ldaos -ldaos_common -lgurt -lcart -luuid -lcmocka -ldaos_tests
    scons: done building targets.
[root@ssc-vm-2051 daos]#


[ Note -- By default, DAOS and its dependencies are installed under ${daospath}/install. The installation path can be modified by adding the PREFIX= option to the above command line (e.g., PREFIX=/usr/local).]

## Set environment

* Export following paths to your .bashrc

    ```~/.bashrc```
    
    ```export daospath=/path/to/your/daos/main/directory``` 

    ```CPATH=${daospath}/install/include/:$CPATH```

    ```PATH=${daospath}/install/bin/:${daospath}/install/sbin:$PATH```

    ```export CPATH PATH```
    
    ```source ~/.bashrc```
    
* Required directory setup

    ```mkdir /var/run/daos_server```
    
    ```chmod 0755 /var/run/daos_server```
    
    ```mkdir /var/run/daos_agent```
    
    ```chmod 0755 /var/run/daos_agent```
    
## Create mount point

DAOS demands 2 kinds of storage. 1 for SCM storage for metadata and NVMe for bulky storage. Right now for testing purpose we are going to emulate SCM with tmpfs only.

* Mount tmpfs

    ```mkdir /mnt/daos```
    
    One may use another mount-point or directory as well.
  
    ```mount -t tmpfs -o size=XXG tmpfs /mnt/daos```

    XX could be number of GB storage one is willing to allocate while mounting tmpfs. 

* Use the 'df' command to verify mounting status.

* Use this [server config file](daos_server.yml) which is having minimum settings to up and running a single node server. Copy this example file's configurations to /etc/daos/daos_server.yml

        Server's default configuration files are located at following locations : 

        /root/daos_src/daos/install/etc/daos_server.yml
        /root/daos_src/daos/utils/config/daos_server.yml


* /mnt/daos is the default location specified under /etc/daos/daos_server.yml file

* Space XX GB should also be specified inside daos_server.yml file

## Start daos server

* Starting a server process in a new terminal can be done using the following command. Please understand that it is okay to run this process in the background.

   ```daos_server start -o /etc/daos/daos_server.yml```
   
        Terminal log --
        
        [root@ssc-vm-2051 daos]# daos_server start -o /etc/daos/daos_server.yml
        DAOS Server config loaded from /etc/daos/daos_server.yml
        daos_server logging to file /tmp/daos_control.log
        DAOS Control Server v1.1.2.1 (pid 510) listening on 0.0.0.0:10001
        Checking DAOS I/O Server instance 0 storage ...
        Metadata format required on instance 0

## Start daos agent

* Starting an agent process in a new terminal can be done using the following command. Please understand that it is okay to run this process in the background.

   ```daos_agent -i```
   
        Agent's default configuration files are located at following locations : 

        /root/daos_src/daos/install/etc/daos_agent.yml
        /root/daos_src/daos/utils/config/daos_agent.yml

   
## Container creation

* Open new terminal and Export variables 

   ```export CRT_PHY_ADDR_STR="ofi+sockets"; export OFI_INTERFACE="lo"```


* On the first time a server process starts, mounted storage space is supposed to be formatted before usage. For this purpose use below command

  ```dmg -i storage format –reformat```
  
        Terminal log --
  
        [root@ssc-vm-2051 daos]# dmg -i storage format --reformat
        Format Summary:
        Hosts     SCM Devices NVMe Devices
        -----     ----------- ------------
        localhost 1           0


* Pool creation

  ```dmg -i pool create -s 1G```
  
  Here the pool of only 1GB space is getting created. one may use other value as well, but that should be within the range of allocated storage.
      
      
      Terminal log --
        [root@ssc-vm-2051 daos]# dmg -i pool create -s 1G
        Creating DAOS pool with manual per-server storage allocation: 1.0 GB SCM, 0 B NVMe (100.00% ratio)
        Pool created with 100.00% SCM/NVMe ratio
        -----------------------------------------
          UUID          : c7b0c9e2-028d-4dde-b016-a68743dba49a
          Service Ranks : 0
          Storage Ranks : 0
          Total Size    : 1.0 GB
          SCM           : 1.0 GB (1.0 GB / rank)
          NVMe          : 0 B (0 B / rank)


      
  ```export PUUID=VALUE_OF_RETURNED_UUID_IN_POOL_CREATE_COMMAND```
  
        i.e. export PUUID=c7b0c9e2-028d-4dde-b016-a68743dba49a
      
* List pool

  ```dmg -i system list-pools```
  
        Terminal log --
        [root@ssc-vm-2051 daos]# dmg -i system list-pools
        Pool UUID                            Svc Replicas
        ---------                            ------------
        c7b0c9e2-028d-4dde-b016-a68743dba49a 0

  
* Create POSIX container

  ```daos container create --pool=$PUUID --path=/path/to/some/non-existing/location --type=POSIX```
        
  Make sure the provided path does not exist, as this path is going to be linked with pool to keep a track of this newly created container.
      
      
        Terminal log --
      
        [root@ssc-vm-2051 daos]# daos container create --pool=$PUUID --path=/tmp/cont1 --type=POSIX
        fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
        fi   WARN src/gurt/fault_inject.c:724 d_fault_attr_set() Fault Injection attr not set feature not included in build
        daos INFO src/client/api/job.c:89 dc_job_init() Using JOBID ENV: DAOS_JOBID
        daos INFO src/client/api/job.c:90 dc_job_init() Using JOBID ssc-vm-2051.colo.seagate.com-1664
        mgmt INFO src/mgmt/cli_mgmt.c:360 dc_mgmt_net_cfg() Using client provided OFI_INTERFACE: lo
        crt  INFO src/cart/crt_init.c:311 crt_init_opt() libcart version 4.9.0 initializing
        fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
        crt  WARN src/cart/crt_init.c:162 data_init() FI_UNIVERSE_SIZE was not set; setting to 2048
        client INFO src/utils/daos.c:168 cmd_args_print()       DAOS system name: daos_server
        client INFO src/utils/daos.c:169 cmd_args_print()       pool UUID: c7b0c9e2-028d-4dde-b016-a68743dba49a
        client INFO src/utils/daos.c:170 cmd_args_print()       cont UUID: 00000000-0000-0000-0000-000000000000
        client INFO src/utils/daos.c:174 cmd_args_print()       pool svc: parsed 0 ranks from input NULL
        client INFO src/utils/daos.c:178 cmd_args_print()       attr: name=NULL, value=NULL
        client INFO src/utils/daos.c:182 cmd_args_print()       path=/tmp/cont1, type=POSIX, oclass=UNKNOWN, chunk_size=0
        client INFO src/utils/daos.c:188 cmd_args_print()       snapshot: name=NULL, epoch=0, epoch range=NULL (0-0)
        client INFO src/utils/daos.c:189 cmd_args_print()       oid: 0.0
        Successfully created container 226b4ee3-c972-4fea-8619-82f30e5bec4b type POSIX
        fi   WARN src/gurt/fault_inject.c:693 d_fault_inject_fini() Fault Injection not finalized feature not included in build
        fi   WARN src/gurt/fault_inject.c:693 d_fault_inject_fini() Fault Injection not finalized feature not included in build
     
     
You should be able to create a posix container using the above source build method.

# CRUD operations on POSIX object

* Steps for creating a posix object, reading, updating and deleting the same is demonstrated below. This activity demands creation of a pool, container and mounting of a container to dfuse for storing an object in the container and modify it just as a normal posix file object.

    - Pool creation & export
    
        Terminal log -
            
            [root@ssc-vm-2051 daos]# dmg -i pool create -s 1G
            Creating DAOS pool with manual per-server storage allocation: 1.0 GB SCM, 0 B NVMe (100.00% ratio)
            Pool created with 100.00% SCM/NVMe ratio
            -----------------------------------------
              UUID          : c7b0c9e2-028d-4dde-b016-a68743dba49a
              Service Ranks : 0
              Storage Ranks : 0
              Total Size    : 1.0 GB
              SCM           : 1.0 GB (1.0 GB / rank)
              NVMe          : 0 B (0 B / rank)

            [root@ssc-vm-2051 daos]#
            [root@ssc-vm-2051 daos]#
            [root@ssc-vm-2051 daos]# dmg -i system list-pools
            Pool UUID                            Svc Replicas
            ---------                            ------------
            c7b0c9e2-028d-4dde-b016-a68743dba49a 0

            [root@ssc-vm-2051 daos]# export pool_id=c7b0c9e2-028d-4dde-b016-a68743dba49a


    - Container creation & export
        
        Terminal logs -

            [root@ssc-vm-2051 daos]# daos container create --pool=$pool_id --path=/tmp/test_container --type=POSIX
            fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
            fi   WARN src/gurt/fault_inject.c:724 d_fault_attr_set() Fault Injection attr not set feature not included in build
            daos INFO src/client/api/job.c:89 dc_job_init() Using JOBID ENV: DAOS_JOBID
            daos INFO src/client/api/job.c:90 dc_job_init() Using JOBID ssc-vm-2051.colo.seagate.com-1664
            mgmt INFO src/mgmt/cli_mgmt.c:360 dc_mgmt_net_cfg() Using client provided OFI_INTERFACE: lo
            crt  INFO src/cart/crt_init.c:311 crt_init_opt() libcart version 4.9.0 initializing
            fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
            crt  WARN src/cart/crt_init.c:162 data_init() FI_UNIVERSE_SIZE was not set; setting to 2048
            client INFO src/utils/daos.c:168 cmd_args_print()       DAOS system name: daos_server
            client INFO src/utils/daos.c:169 cmd_args_print()       pool UUID: c7b0c9e2-028d-4dde-b016-a68743dba49a
            client INFO src/utils/daos.c:170 cmd_args_print()       cont UUID: 00000000-0000-0000-0000-000000000000
            client INFO src/utils/daos.c:174 cmd_args_print()       pool svc: parsed 0 ranks from input NULL
            client INFO src/utils/daos.c:178 cmd_args_print()       attr: name=NULL, value=NULL
            client INFO src/utils/daos.c:182 cmd_args_print()       path=/tmp/test_container, type=POSIX, oclass=UNKNOWN, chunk_size=0
            client INFO src/utils/daos.c:188 cmd_args_print()       snapshot: name=NULL, epoch=0, epoch range=NULL (0-0)
            client INFO src/utils/daos.c:189 cmd_args_print()       oid: 0.0
            Successfully created container 226b4ee3-c972-4fea-8619-82f30e5bec4b type POSIX
            fi   WARN src/gurt/fault_inject.c:693 d_fault_inject_fini() Fault Injection not finalized feature not included in build
            fi   WARN src/gurt/fault_inject.c:693 d_fault_inject_fini() Fault Injection not finalized feature not included in build
            [root@ssc-vm-2051 daos]#

            [root@ssc-vm-2051 daos]# export container_id=226b4ee3-c972-4fea-8619-82f30e5bec4b

# Mount container using dfuse

* Create new directory to mount a container

    ```mkdir /mnt/rajkumar/dfuse_t_container```

* Mount containers

    ```dfuse -m /mnt/rajkumar/dfuse_t_container --pool $pool_id --cont $container_id```

        [root@ssc-vm-2051 daos]# dfuse -m /mnt/rajkumar/dfuse_t_container --pool $pool_id --cont $container_id
        fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
        fi   WARN src/gurt/fault_inject.c:724 d_fault_attr_set() Fault Injection attr not set feature not included in build
        daos INFO src/client/api/job.c:89 dc_job_init() Using JOBID ENV: DAOS_JOBID
        daos INFO src/client/api/job.c:90 dc_job_init() Using JOBID ssc-vm-2051.colo.seagate.com-7259
        mgmt INFO src/mgmt/cli_mgmt.c:360 dc_mgmt_net_cfg() Using client provided OFI_INTERFACE: lo
        crt  INFO src/cart/crt_init.c:311 crt_init_opt() libcart version 4.9.0 initializing
        fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
        crt  WARN src/cart/crt_init.c:162 data_init() FI_UNIVERSE_SIZE was not set; setting to 2048
        duns INFO src/client/dfs/duns.c:393 duns_resolve_path() Path does not represent a DAOS link
        dfuse INFO src/client/dfuse/dfuse_main.c:457 main(0x824000) duns_resolve_path() returned 61 No data available
        dfuse INFO src/client/dfuse/dfuse_main.c:60 dfuse_send_to_fg() Sending 0 to fg

* Create objects (files) inside container

    ```cd /mnt/rajkumar/dfuse_t_container```
        
    ```touch fileA fileB```
        
     Checking directory and populating contents of posix objects (files) -
        
        [root@ssc-vm-2051 dfuse_t_container]# ls
        fileA  fileB
        [root@ssc-vm-2051 dfuse_t_container]# echo "hello world!" > fileA
        [root@ssc-vm-2051 dfuse_t_container]# echo "hello universe!" > fileB
        
* Read object

        [root@ssc-vm-2051 dfuse_t_container]# cat fileA
        hello world!
        [root@ssc-vm-2051 dfuse_t_container]# cat fileB
        hello universe!
        
* Update object

        [root@ssc-vm-2051 dfuse_t_container]# echo "new line added to the world!" >> fileA
        [root@ssc-vm-2051 dfuse_t_container]# cat fileA
        hello world!
        new line added to the world!
    
* Delete object

        [root@ssc-vm-2051 dfuse_t_container]# rm fileA
        [root@ssc-vm-2051 dfuse_t_container]# ls
        fileB

This is how we create a pool, create a container and after mounting the same to dfuse, we can create, read, update and delete POSIX objects.
