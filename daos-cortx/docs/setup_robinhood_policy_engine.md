# Introduction

Robinhood Policy Engine is a versatile tool to manage contents of large file systems. It maintains a replica of file system metadata in a database that can be queried at will. for more details kindly check [Robinhood wiki](https://github.com/cea-hpc/robinhood/wiki) page.

# Setup guide

Complete details for setup are available [here](https://github.com/cea-hpc/robinhood/wiki/robinhood_v3_admin_doc#software-installation)

Still, basic steps are provided here for quick reference with posix support.

* Build dependencies 

      Install build requirements:
       yum install -y git autogen rpm-build autoconf automake gcc libtool \
                      glib2-devel libattr-devel mariadb-devel mailx bison flex
                
- Reference is also available [here]( https://github.com/cea-hpc/robinhood/wiki/robinhood_v3_admin_doc#build-and-installation-from-sources)
                
* Download source code

- Make sure to use commands as per your curren robinhood version.

`weget https://sourceforge.net/projects/robinhood/files/latest/download/robinhood/3.1.6/robinhood-3.1.6.tar.gz`

`tar zxf robinhood-3.1.6.tar.gz`
 
`cd  robinhood-3.1.6`

Note : Here, source is cloned inside /root/setup_robinhood/ path and same will be referenced in the following commands. so make sure you use your own path.

* build robinhood RPMs by running
 
`./configure`
  
  - install missing deps -- mycase yum install jemalloc-devel.x86_64 jemalloc.x86_64
  
`make rpm`

* install and start database service

`yum install mariadb-server`

`systemctl start mariadb.service`

* Creating robinhood database 

`/root/setup_robinhood/robinhood-3.1.6/scripts/rbh-config create_db <db_name>    'localhost' 'rbh_password'`

A common name for robinhood database name is 'rbh_fsname'. Write the selected password to a file only readable by 'root' (600), for example in /etc/robinhood.d/.dbpassword.

Reference is available [here](https://github.com/cea-hpc/robinhood/wiki/v3_posix_tuto#configuration)

* Create a robinhood configuration file, starting with a simple robinhood template:

`cp /root/setup_robinhood/robinhood-3.1.6/doc/templates/basic.conf /etc/robihood.d/posix.conf`

* Edit the configuration file

In 'General' block, set filesystem root path, and the corresponding file system type.
       
       fs_path = "/fs/root";
       fs_type = xfs;
 
* In 'ListManager' block, set database connection parameters:

      db = rbh_fsname;
      password_file = "/etc/robinhood.d/.dbpassword" ;

It is recommended to define your fileclasses before running the initial file system scan.

This way, you will get relevant information in 'rbh-report --class-info' report after the initial scan is completed.

    fileclass empty_file {
        definition { type == file and size == 0 }
     }
     fileclass small_file {
        definition { type == file
                 and size > 0
                 and size <= 32MB }
     }

Reference config file is available [here](https://github.com/Seagate/cortx-experiments/blob/rajkumarpatel2602-robinhood-pengine/daos-cortx/src/samples/posix.conf)
Make sure to make above relevant changes in fields mentioned above.

* Start Robinhood scan and update

 `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/posix.conf`

* Query database
 
 `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/rbh-report --fs-info --class-info`
 
## Test for daos to CORTX and vice-versa data movement

In this exercise object movements from daos to cortx and cortx to daos will be made sure. This exercise will be carried out by defining policies inside a container and running those policies using robinhood policy engine. There are two prerequisites to carry out this test mentioned below.

* Daos server node running on one VM

  - follow this [document](https://github.com/Seagate/cortx-experiments/blob/main/daos-cortx/docs/setup_daos.md) to setup daos and creating container.
  
* Cortx server node running on second VM

  - follow this [document](https://github.com/Seagate/cortx/blob/main/QUICK_START.md) to setup cortx on your vm.
  
* Once everything is in-place let's start with the data movement test by following the steps below on daos node which is hosting robinhood policy engine.
 
1. Create objects in a daos container (i.e. inside dfuse mount point)

- create larger and smaller objects inside the container. container is mounted at /mnt/daos_container for this excercise and same fs_path will be used in config file as well.

- These object(s) are going to be moved to s3 bucket and downloaded from there to doas container directory.

2. Create config file and add policies and start Scanning the database and check contents of the container on robinhood's database

- Readily available config files with correct config options are present [here](https://github.com/Seagate/cortx-experiments/blob/rajkumarpatel2602-robinhood-pengine/daos-cortx/src/samples/rh_daos_cortx.conf)

`/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/rh_daos_cortx.conf`

`/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/rbh-report --fs-info --class-info`
 
3. Create s3 bucket 
 
`aws s3 mb s3://daos-bucket`

Note : For this excercise test buacket name used is daos-bucket and same is used inside rh_daos_cortx.conf file referenced above.

4. Run the policy to move larger objects (daos_to_cortx_archive policy)

`/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/rh_daos_cortx.conf --run=daos_to_cortx_archive(all)`

5. Verify contents on container and on s3 bucket

`ls`

`aws s3 ls s3://daos-bucket`

This is how we have successfully moved larger objects (size > 1MB) from daos to cortx

6. Run the policy to move objects from cortx to daos(run cortx_to_daos_restore policy)

`/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/rh_daos_cortx.conf --run=cortx_to_daos_restore(all)`

7. Verify contents on container and on s3 bucket

`ls`

`aws s3 ls s3://daos-bucket`

So, This is how we have successfully moved objects from s3 bucket to daos container.
