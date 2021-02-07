# Introduction

Robinhood Policy Engine is a versatile tool to manage contents of large file systems. It maintains a replicate of filesystem medatada in a database that can be queried at will. for more details kindly check [Robinhood wiki](https://github.com/cea-hpc/robinhood/wiki) page.

# Setup guide

Complete details for setup are available [here](https://github.com/cea-hpc/robinhood/wiki/robinhood_v3_admin_doc#software-installation)

Still, basic steps are provided here for quick reference with posix support.

* Build dependencies // https://github.com/cea-hpc/robinhood/wiki/robinhood_v3_admin_doc#build-and-installation-from-sources

      Install build requirements:
       yum install -y git autogen rpm-build autoconf automake gcc libtool \
                      glib2-devel libattr-devel mariadb-devel mailx bison flex
                
* Download source code

`weget https://sourceforge.net/projects/robinhood/files/latest/download/robinhood/3.1.6/robinhood-3.1.6.tar.gz`

`tar zxf robinhood-3.1.6.tar.gz // use your version`
 
`cd  robinhood-3.1.6`
 
*  build robinhood RPMs by running:
 
`./configure`
  
  - install missing deps -- mycase yum install jemalloc-devel.x86_64 jemalloc.x86_64
  
`make rpm`

* install and start database service

`yum install mariadb-server`

`systemctl start mariadb.service`

* Creating robinhood database //https://github.com/cea-hpc/robinhood/wiki/v3_posix_tuto#configuration

rbh-config create_db <db_name>    'localhost' 'rbh_password' // /root/setup_robinhood/robinhood-3.1.6/scripts/rbh-config rbh_fsname  'localhost' 'rbh_password'

A common name for robinhood database name is 'rbh_fsname.
Write the selected password to a file only readable by 'root' (600), for example in /etc/robinhood.d/.dbpassword.

* Create a robinhood configuration file, starting with a simple robinhood template:

cp /root/setup_robinhood/robinhood-3.1.6/doc/templates/basic.conf /etc/robihood.d/posix.conf

* Edit the configuration file

n 'General' block, set filesystem root path, and the corresponding filesystem type:
 fs_path = "/fs/root";
 fs_type = xfs;
 
* In 'ListManager' block, set database connection parameters:

db = <db_name>;
password_file = "/etc/robinhood.d/.dbpassword" ;

It is recommended to define your fileclasses before running the initial filesystem scan:

This way, you will get relevent information in 'rbh-report --class-info' report after the initial scan is completed.

    fileclass empty_file {
        definition { type == file and size == 0 }
     }
     fileclass small_file {
        definition { type == file
                 and size > 0
                 and size <= 32MB }
     }

* start scan

 `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/posix.conf`

 * info
 
 `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/rbh-report --fs-info --class-info`
 
##TEST WITH DAOS_CORTX

In this excercise object movements from daos to cortx and cortx to daos will be made sure. This exercise will be carried out by defining policies inside a container and running those policies using robinhood policy engine. There are two pre-requisites to carry out this test mentioned below.
* daos server node running on one VM

  - follow this document to setup daos and creating container.
  
* cortx server node running on second VM

  - follow this document to setup cortx on your vm.
  
* once everything is in-place let's start with the datamovement test by following below steps on daos node which is running robinhood policy engine.
 
1. create obejcts in a daos container (i.e. inside dfuse mount point)

These object(s) are going to be moved to s3 bucket and downloaded from there to doas container directory

2. scan the database and check contents of the container on robinhood's database

`/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/posix.conf`

`/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/rbh-report --fs-info --class-info`
 
3. create s3 bucket 
 
`aws s3 mb s3://daos-perf-test-bucket`

4. run the policy to move larger obejcts (daos_to_cortx_archive policy)

`/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/posix.conf --run=daos_cortx(all)`

5. check contents on cotainer and on s3 bucket

`ls`

`aws s3 ls s3://daos-bucket`

This is how we have successfully moved larger objects (size > 1MB) from daos to cortx

6. run the policy to move objects from cortx to daos(run cortx_to_daos_restore policy)

check contents on container and on s3 bucket

`ls`

`aws s3 ls s3://daos-bucket`

THis is how we have successfully moved objects from s3 bucket to daos container.
