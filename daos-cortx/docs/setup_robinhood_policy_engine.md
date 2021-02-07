Introduction

Setup guide

details are at  : https://github.com/cea-hpc/robinhood/wiki/robinhood_v3_admin_doc#software-installation

1. build dependencies // https://github.com/cea-hpc/robinhood/wiki/robinhood_v3_admin_doc#build-and-installation-from-sources

Install build requirements:
 yum install -y git autogen rpm-build autoconf automake gcc libtool \
                glib2-devel libattr-devel mariadb-devel mailx bison flex
                
2. download source code

weget https://sourceforge.net/projects/robinhood/files/latest/download/robinhood/3.1.6/robinhood-3.1.6.tar.gz

 tar zxf robinhood-3.1.6.tar.gz // use your version
 
 cd  robinhood-3.1.6
 
 3. build robinhood RPMs by running:
 
  ./configure
  
  install missing deps -- mycase yum install jemalloc-devel.x86_64 jemalloc.x86_64
  
  make rpm

4. install and start database service

yum install mariadb-server

systemctl start mariadb.service

5. Creating robinhood database //https://github.com/cea-hpc/robinhood/wiki/v3_posix_tuto#configuration

rbh-config create_db <db_name>    'localhost' 'rbh_password' // /root/setup_robinhood/robinhood-3.1.6/scripts/rbh-config rbh_fsname  'localhost' 'rbh_password'

A common name for robinhood database name is 'rbh_fsname.
Write the selected password to a file only readable by 'root' (600), for example in /etc/robinhood.d/.dbpassword.

6. Create a robinhood configuration file, starting with a simple robinhood template:

cp /root/setup_robinhood/robinhood-3.1.6/doc/templates/basic.conf /etc/robihood.d/posix.conf

7. Edit the configuration file

n 'General' block, set filesystem root path, and the corresponding filesystem type:
 fs_path = "/fs/root";
 fs_type = xfs;
 
8. In 'ListManager' block, set database connection parameters:

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
 
9. feeding robinhood
 

10. start scan

 /root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/robinhood --scan --once -L stderr -f /etc/robinhood.d/posix.conf


 11. info
 
 /root/setup_robinhood/robinhood-3.1.6/rpms/BUILD/robinhood-3.1.6/src/robinhood/rbh-report --fs-info
 
##TEST WITH DAOS_CORTX
 
 N
 
 
 
 
 
