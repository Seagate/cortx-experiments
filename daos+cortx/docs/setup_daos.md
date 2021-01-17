# System requirements

# DAOS installation methods

There are three ways to install daos server and client on your machine.
- RPM based
- DOCKER
- Source build method

source based method is discussed below.

# DAOS single-node server setup

Source based setup method: (follow -- https://daos-stack.github.io/admin/installation/#daos-from-scratch)

## Install dependencies // Specific to CentOS / RHEL

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

## clone repo

* For the current development version,

  ```git clone --recurse-submodules https://github.com/daos-stack/daos.git```

* To checkout the latest stable version,

  ```git clone --recurse-submodules -b v1.0.1 https://github.com/daos-stack/daos.git```
  
## build daos

```cd daos```

```cd scons --config=force --build-deps=yes install```

[ Note -- By default, DAOS and its dependencies are installed under ${daospath}/install. The installation path can be modified by adding the PREFIX= option to the above command line (e.g., PREFIX=/usr/local).]

## set environment

* Export following paths to your .bashrc

    ```export daospath=/path/to/your/daos/main/directory``` 

    ```CPATH=${daospath}/install/include/:$CPATH```

    ```PATH=${daospath}/install/bin/:${daospath}/install/sbin:$PATH```

    ```export CPATH PATH``` 
    
* required directory setup

    ```mkdir /var/run/daos_server```
    ```chmod 0755 /var/run/daos_server```
    ```mkdir /var/run/daos_agent```
    ```chmod 0755 /var/run/daos_agent```
    
## Create mount point for tmpfs

DAOS demands 2 kind of storage. 1 for SCM storage for metadata and NVMe for bulky storage. Right now for testing purpose we are going to emulate SCM with tmpfs only.

* mount tmpfs
  
    ```mount -t tmpfs -o size=XXG tmpfs /mnt/daos```

       (make sure /mnt/daos is created and not in use.) 

* use 'df' command to verify mounting status.

* /mnt/daos is the default location specified under /etc/daos/daos_server.yml file

* Space XX GB should also be specified inside daos_server.yml file

## start daos server

* starting a server process in new terminal can be done using following command. please do understand that it is okay to run this process in background.

   ```daos_server start -o /etc/daos/daos_server.yml```
   
## start agent

* starting an agnet process in new terminal can be done using following command. please do understand that it is okay to run this process in background.

   ```daos_agent -i -o /etc/daos/daos_agent.yml```
   
## Container creation

* Open new terminal and Export variables 

   ```export CRT_PHY_ADDR_STR="ofi+sockets"; export OFI_INTERFACE="lo"```


* On the first time of server process starting mounted storage space is supposed to be formatted before usage. for this purpose use below command

  ```dmg -i storage format –reformat```

* Pool creation

  ```dmg -i pool create -s 1G```
  
      Here pool of only 1GB space is getting created. one may use other value as well, but that should be within range of allocated storage.
      
  ```export pool=VALUE_OF_RETURNED_UUID_IN_POOL_CREATE_COMMAND```
      
* list pool

  ```dmg -i system list-pools```
  
* create POSIX container

  ```daos container create --pool=$PUUID --path=/path/to/some/non-existing/location --type=POSIX```
  
      Make sure provided path does not exist, as this path is going to be linked with pool to keep a track of this newly created container.
     
     
      You should be able to create a posix container using above source build method. Now one can create posix object (I.e., typical files) inside the container.
