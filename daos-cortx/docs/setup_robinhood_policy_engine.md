# Introduction

  Robinhood Policy Engine is a versatile tool to manage contents of large file systems. It maintains a replica of file system metadata in a database that can be queried at will. for more details kindly check [Robinhood wiki](https://github.com/cea-hpc/robinhood/wiki) page.

# Setup guide

  Complete details for setup are available [here.](https://github.com/cea-hpc/robinhood/wiki/robinhood_v3_admin_doc#software-installation)

  Still, basic steps are provided here for quick reference with posix support.

* Build dependencies 

      Install build requirements:
       yum install -y git autogen rpm-build autoconf automake gcc libtool \
                      glib2-devel libattr-devel mariadb-devel mailx bison flex
                
  Reference is also available [here.]( https://github.com/cea-hpc/robinhood/wiki/robinhood_v3_admin_doc#build-and-installation-from-sources)
                
* Download source code

  Make sure to use commands as per your curren robinhood version.

      `wget https://sourceforge.net/projects/robinhood/files/latest/download/robinhood/3.1.6/robinhood-3.1.6.tar.gz`

      `tar zxf robinhood-3.1.6.tar.gz`
 
      `cd  robinhood-3.1.6`

  Note : Here, source is cloned inside /root/setup_robinhood/ path and same will be referenced in the following commands. so make sure you use your own path.

* Build robinhood RPMs by running
 
      `./configure`
  
* Install missing deps -- mycase yum install jemalloc-devel.x86_64 jemalloc.x86_64
  
      `make rpm`

* Install and start database service

      `yum install mariadb-server`

      `systemctl start mariadb.service`

* Creating robinhood database 

      `/root/setup_robinhood/robinhood-3.1.6/scripts/rbh-config create_db <db_name>    'localhost' 'rbh_password'`

  A common name for robinhood database name is 'rbh_fsname'. Write the selected password to a file only readable by 'root' (600), for example in /etc/robinhood.d/.dbpassword.

  Reference is available [here.](https://github.com/cea-hpc/robinhood/wiki/v3_posix_tuto#configuration)

* Create a robinhood configuration file, starting with a sample robinhood template:

      `cp /root/setup_robinhood/robinhood-3.1.6/doc/templates/basic.conf /etc/robihood.d/posix.conf`

* Edit the configuration file

  In 'General' block, set filesystem path to be scanned by Robinhood policy engine.
       
       fs_path = "/mnt/src_container_mnt";
       fs_type = fuse.daos;
       
  Note : Make sure you use filesystem path of your interest.
 
  In 'ListManager' block, set database connection parameters:

      db = rbh_fsname;
      password_file = "/etc/robinhood.d/.dbpassword" ;

  It is recommended to define your fileclasses before running the initial file system scan.

  This way, you will get relevant information in 'rbh-report --class-info' report after the initial scan is completed. 3 Example file-classes are give below.

      fileclass all_object {
                definition { size > 0 }
      }

      fileclass big_object {
                definition { size > 1MB }
      }

      fileclass small_object {
                definition { size < 1MB}
      }


  Reference config file is available [here.](https://github.com/Seagate/cortx-experiments/blob/main/daos-cortx/src/samples/rh_daos_cortx.conf)
  
  Make relevant changes in fields mentioned above.

* Start Robinhood scan and update

      `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/rh_daos_cortx.conf`

* Query database
 
      `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/rbh-report --fs-info --class-info -f /etc/robinhood.d/rh_daos_cortx.conf`
 
# Test for daos to CORTX and vice-versa data movement

In this exercise object movements from daos to cortx and cortx to daos will be made sure. This exercise will be carried out by defining policies inside a container and running those policies using robinhood policy engine. There are two prerequisites to carry out this test mentioned below.

Node : There's a demonstration video available for the following exercise[here](). //TODO

* Daos server node running on one VM

  Follow this [document](https://github.com/Seagate/cortx-experiments/blob/main/daos-cortx/docs/setup_daos.md) to setup daos and creating container.
  
* Cortx server node running on second VM

  Follow this [document](https://github.com/Seagate/cortx/blob/main/QUICK_START.md) to setup cortx on your vm.
  
* Once everything is in-place let's start with the data movement test by following the steps below on daos node which is hosting robinhood policy engine.
 
1. Create objects in a daos container

   Create a pool and 2 containers inside that pool. Create dfuse mount points for both containers.
   
   For this exercise, mount points are /mnt/src_container_mnt and /mnt/dest_container_mnt.

      `[root@daos-node ~]# cd /mnt/src_container_mnt`
   
   Create a small object (<1MB) and a big object(>1MB) inside a container.
   
            dd if=/dev/urandom bs=100 count=1 | base64 > ./small_object
   
            dd if=/dev/urandom bs=1024 count=2048 | base64 > ./big_object
            
   Verify contents
   
         [root@daos-node src_container_mnt]# ls
         big_object samll_object

   Large object files (>1MB) residing /mnt/src_container_mnt will be archived to cortx-s3 bucket and all objects inside bucket will be restored to /mnt/dest_container_mnt using robinhood policy engine.

2. Create config file and add policies and start Scanning the database and check contents of the container on robinhood's database

   Readily available config file with correct config options are present [here.](https://github.com/Seagate/cortx-experiments/blob/main/daos-cortx/src/samples/rh_daos_cortx.conf)
   
   There are two policies added for archive and restore operation of the objects from daos to cortx node and cortx to daos.
   
   Archive Policy :
   
        #daos_to_cortx_archive -- aws s3 mv
        define_policy daos_to_cortx_archive{
             status_manager = none;
             scope=all;
             default_action = cmd("aws s3 ls");
             default_lru_sort_attr = none;
        }

        daos_to_cortx_archive_rules{
            rule big_movement{
              target_fileclass = big_object;
              action = cmd("aws s3 mv /mnt/src_container_mnt/{name} s3://daos-bucket");
              condition { last_access < 1d }
            }
        }
        
    Restore Policy :
    
        #cortx_to_daos_restore -- aws s3 mv from bucket to daos container
        define_policy cortx_to_daos_restore{
             status_manager = none;
             scope=all;
             default_action = cmd("aws s3 ls");
             default_lru_sort_attr = none;
        }

        cortx_to_daos_restore_rules{
            rule s3_move_operation{
              target_fileclass = all_object;
              action = cmd("aws s3 mv s3://daos-bucket/ /mnt/dest_container_mnt/ --recursive");
              condition { last_access < 1d }
            }
        }
        
   Trigger scan and query report to check latest entries inside fs_path(i.e. /mnt/src_container_mnt).

      `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/rh_daos_cortx.conf`

      `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/rbh-report --fs-info --class-info -f /etc/robinhood.d/rh_daos_cortx.conf`
 
3. Create s3 bucket 
 
      `[root@daos-node src_container_mnt]# aws s3 mb s3://daos-bucket`

   Note : For this exercise test bucket name used is daos-bucket and same is used inside rh_daos_cortx.conf file referenced above.

4. Run the policy to move larger objects (daos_to_cortx_archive policy)

      `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/rh_daos_cortx.conf --run=daos_to_cortx_archive(all)`

5. Verify contents on source container and on s3 bucket

        [root@daos-node src_container_mnt]# ls
        small_object
        [root@daos-node src_container_mnt]# aws s3 ls s3://daos-bucket
        2021-03-03 00:47:02    2832997 big_object

   This is how we have successfully moved larger objects (size > 1MB) from daos to cortx
   
        [root@daos-node src_container_mnt]# cd /mnt/dest_cotntainer_mnt
        [root@daos-node dest_container_mnt]# ls
        [root@daos-node dest_container_mnt]# 
            
   At the moment, no objects are present inside dest_container_mnt.

6. Run the policy to move objects from cortx to daos(run cortx_to_daos_restore policy)

      `/root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/rh_daos_cortx.conf --run=cortx_to_daos_restore(all)`

7. Verify contents on container and on s3 bucket

        [root@daos-node dest_container_mnt]# ls
        big_object
        [root@daos-node dest_container_mnt]# aws s3 ls s3://daos-bucket
        [root@daos-node dest_container_mnt]# 

So, This is how we have successfully moved objects from s3 bucket to daos container.
