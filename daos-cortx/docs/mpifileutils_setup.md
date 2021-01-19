# Pre-requisites

* cmake version 3.1 or more required.

    ```yum install cmake3```
        
    To verify -
        
    ```cmake3 --version```
        
        Terminal logs -
        
        [root@ssc-vm-2051 daos]# cmake3 --version
        cmake3 version 3.17.5

        CMake suite maintained and supported by Kitware (kitware.com/cmake).

* Install openmpi

    ```yum -y install openmpi3-devel```

        Terminal's ending logs -
        
        Downloading packages:
        openmpi-1.10.7-5.el7.x86_64.rpm                                                                                                       | 3.1 MB  00:00:00
        Running transaction check
        Running transaction test
        Transaction test succeeded
        Running transaction
          Installing : openmpi-1.10.7-5.el7.x86_64                                                                                                               1/1
        Loaded plugins: fastestmirror, product-id, subscription-manager
          Verifying  : openmpi-1.10.7-5.el7.x86_64                                                                                                               1/1

        Installed:
          openmpi.x86_64 0:1.10.7-5.el7

        Complete!


   To verify -
        
    ```ls /usr/lib64/openmpi3/bin/```
        
        Terminal's log -
        
        [root@ssc-vm-2051 daos]# ls /usr/lib64/openmpi3/bin/
    
        aggregate_profile.pl  mpif77                ompi_info             orte-clean            orte-server           oshfort               shmemcc
        mpic++                mpif90                ompi-ps               orted                 orte-top              oshmem_info           shmemCC
        mpicc                 mpifort               ompi-server           orte-dvm              oshc++                oshrun                shmemcxx
        mpiCC                 mpirun                ompi-top              orte-info             oshcc                 profile2mat.pl        shmemfort
        mpicxx                ompi-clean            opal_wrapper          orte-ps               oshCC                 prun                  shmemrun
        mpiexec               ompi-dvm              ortecc                orterun               oshcxx                shmemc++

* Add path

     ```export PATH=/usr/lib64/openmpi3/bin/:$PATH```

    To verify -
        
     ```which mpicc```
        
        Terminal logs -

        [root@ssc-vm-2051 daos]# which mpicc
        /usr/lib64/openmpi3/bin/mpicc

# Install dependencies

* Make a directory for your setup

    ```mkdir mpifileutils_src```

* Create a build script

    ```touch build_deps.sh```
    
    - To get the latest contents for buuld script, kindly checkout mpifileutil's github-repo[https://github.com/hpc/mpifileutils/blob/master/doc/rst/build.rst]
    
    - Copy contents from above locations to build scripts.
    
            Sample build scripts is presented here[../src/samples/build_deps.sh]

*  Run build script

    ```sh build_deps.sh```

    Terminal logs -
        
         /bin/mkdir -p '/root/mpifileutils_src/install/bin'
          /bin/sh ./libtool   --mode=install /bin/install -c bsdtar bsdcpio bsdcat '/root/mpifileutils_src/install/bin'
        libtool: install: /bin/install -c bsdtar /root/mpifileutils_src/install/bin/bsdtar
        libtool: install: /bin/install -c bsdcpio /root/mpifileutils_src/install/bin/bsdcpio
        libtool: install: /bin/install -c bsdcat /root/mpifileutils_src/install/bin/bsdcat
         /bin/mkdir -p '/root/mpifileutils_src/install/include'
         /bin/install -c -m 644 libarchive/archive.h libarchive/archive_entry.h '/root/mpifileutils_src/install/include'
         /bin/mkdir -p '/root/mpifileutils_src/install/share/man/man1'
         /bin/install -c -m 644 tar/bsdtar.1 cpio/bsdcpio.1 cat/bsdcat.1 '/root/mpifileutils_src/install/share/man/man1'
         /bin/mkdir -p '/root/mpifileutils_src/install/share/man/man3'
         /bin/install -c -m 644 libarchive/archive_entry.3 libarchive/archive_entry_acl.3 libarchive/archive_entry_linkify.3 libarchive/archive_entry_misc.3 libarchive/archive_entry_paths.3 libarchive/archive_entry_perms.3 libarchive/archive_entry_stat.3 libarchive/archive_entry_time.3 libarchive/archive_read.3 libarchive/archive_read_add_passphrase.3 libarchive/archive_read_data.3 libarchive/archive_read_disk.3 libarchive/archive_read_extract.3 libarchive/archive_read_filter.3 libarchive/archive_read_format.3 libarchive/archive_read_free.3 libarchive/archive_read_header.3 libarchive/archive_read_new.3 libarchive/archive_read_open.3 libarchive/archive_read_set_options.3 libarchive/archive_util.3 libarchive/archive_write.3 libarchive/archive_write_blocksize.3 libarchive/archive_write_data.3 libarchive/archive_write_disk.3 libarchive/archive_write_filter.3 libarchive/archive_write_finish_entry.3 libarchive/archive_write_format.3 libarchive/archive_write_free.3 libarchive/archive_write_header.3 libarchive/archive_write_new.3 libarchive/archive_write_open.3 libarchive/archive_write_set_options.3 libarchive/archive_write_set_passphrase.3 libarchive/libarchive.3 libarchive/libarchive_changes.3 libarchive/libarchive_internals.3 '/root/mpifileutils_src/install/share/man/man3'
         /bin/mkdir -p '/root/mpifileutils_src/install/share/man/man5'
         /bin/install -c -m 644 libarchive/cpio.5 libarchive/libarchive-formats.5 libarchive/mtree.5 libarchive/tar.5 '/root/mpifileutils_src/install/share/man/man5'
         /bin/mkdir -p '/root/mpifileutils_src/install/lib/pkgconfig'
         /bin/install -c -m 644 build/pkgconfig/libarchive.pc '/root/mpifileutils_src/install/lib/pkgconfig'
        make[2]: Leaving directory `/root/mpifileutils_src/deps/libarchive-3.5.1'
        make[1]: Leaving directory `/root/mpifileutils_src/deps/libarchive-3.5.1'
        [root@ssc-vm-2051 mpifileutils_src]#


# Build mpifileutils source

* Make sure daos setup and building is already done using these steps[setup_daos.md].

* build latest mpiFileUtils from the master branch with DAOS Support
    

    ```git clone --depth 1 https://github.com/hpc/mpifileutils```
    
    - Commands are also availble inside command at github-repo[https://github.com/hpc/mpifileutils/blob/master/doc/rst/build.rst]
    
            Terminal logs -
    
            [root@ssc-vm-2051 mpifileutils_src]# git clone --depth 1 https://github.com/hpc/mpifileutils
            Cloning into 'mpifileutils'...
            remote: Enumerating objects: 243, done.
            remote: Counting objects: 100% (243/243), done.
            remote: Compressing objects: 100% (202/202), done.
            remote: Total 243 (delta 37), reused 109 (delta 11), pack-reused 0
            Receiving objects: 100% (243/243), 430.01 KiB | 0 bytes/s, done.
            Resolving deltas: 100% (37/37), done.

    ```mkdir build```

    ```cd build```

* Build mpifileutils

    ```cmake3 ../mpifileutils -DWITH_DTCMP_PREFIX=../install -DWITH_LibCircle_PREFIX=../install -DWITH_CART_PREFIX=/root/src_daos/daos/install -DWITH_DAOS_PREFIX=/root/src_daos/daos/install -DCMAKE_INSTALL_PREFIX=../install -DENABLE_DAOS=ON```
    
    
    - Make sure to provide </path/to/daos/source>/install directory. In above example path to daos source is /root/src_daos/daos. 
    
    
    - NOTE - This might give some errors due to missing packages. kindly add those packages.
    
    
    - For an instance some may lack bzip2 packages on their systems and due to that error reproduced would be like below -
    
    
             -- Found CART: /root/daos_src/daos/install/lib64/libcart.so
            /root/daos_src/daos/install/include
            -- Found DAOS: /root/daos_src/daos/install/lib64/libdaos.so
            -- Found LibCircle: /root/mpifileutils_src/install/lib/libcircle.so
            CMake Error at /usr/share/cmake3/Modules/FindPackageHandleStandardArgs.cmake:164 (message):
              Could NOT find BZip2 (missing: BZIP2_LIBRARIES BZIP2_INCLUDE_DIR)
            Call Stack (most recent call first):
              /usr/share/cmake3/Modules/FindPackageHandleStandardArgs.cmake:445 (_FPHSA_FAILURE_MESSAGE)
              /usr/share/cmake3/Modules/FindBZip2.cmake:63 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
              CMakeLists.txt:114 (FIND_PACKAGE)

    - Install such packages using yum
    
       Suppose, to install bzip2 using below commands.
        
    ```yum install bzip2```
    
    ```yum install bzip2-devel.x86_64```

    - Try cmake again
    
    ```[root@ssc-vm-2051 build]#  cmake3 ../mpifileutils -DWITH_DTCMP_PREFIX=../install -DWITH_LibCircle_PREFIX=../install -DWITH_CART_PREFIX=/root/daos_src/daos/install -DWITH_DAOS_PREFIX=/root/daos_src/daos/install -DCMAKE_INSTALL_PREFIX=../install -DENABLE_DAOS=ON```

        Terminal logs -
        
        [root@ssc-vm-2051 build]#  cmake3 ../mpifileutils -DWITH_DTCMP_PREFIX=../install -DWITH_LibCircle_PREFIX=../install -DWITH_CART_PREFIX=/root/daos_src/daos/install -D
        WITH_DAOS_PREFIX=/root/daos_src/daos/install -DCMAKE_INSTALL_PREFIX=../install -DENABLE_DAOS=ON
        -- The C compiler identification is GNU 4.8.5
        -- The CXX compiler identification is GNU 4.8.5
        -- Check for working C compiler: /bin/cc
        -- Check for working C compiler: /bin/cc - works
        -- Detecting C compiler ABI info
        -- Detecting C compiler ABI info - done
        -- Detecting C compile features
        -- Detecting C compile features - done
        -- Check for working CXX compiler: /bin/c++
        -- Check for working CXX compiler: /bin/c++ - works
        -- Detecting CXX compiler ABI info
        -- Detecting CXX compiler ABI info - done
        -- Detecting CXX compile features
        -- Detecting CXX compile features - done
        -- Looking for byteswap.h
        -- Looking for byteswap.h - found
        -- Found MPI_C: /usr/lib64/openmpi3/lib/libmpi.so (found version "3.1")
        -- Found MPI_CXX: /usr/lib64/openmpi3/lib/libmpi_cxx.so (found version "3.1")
        -- Found MPI: TRUE (found version "3.1")
        -- MPI C Compile Flags:  -pthread
        -- MPI C Include Path:   /usr/include/openmpi3-x86_64
        -- MPI C Link Flags:     -Wl,-rpath -Wl,/usr/lib64/openmpi3/lib -Wl,--enable-new-dtags -pthread
        -- MPI C Libraries:      /usr/lib64/openmpi3/lib/libmpi.so
        -- MPI CXX Compile Flags: -pthread
        -- MPI CXX Include Path:  /usr/include/openmpi3-x86_64
        -- MPI CXX Link Flags:    -Wl,-rpath -Wl,/usr/lib64/openmpi3/lib -Wl,--enable-new-dtags -pthread
        -- MPI CXX Libraries:     /usr/lib64/openmpi3/lib/libmpi_cxx.so;/usr/lib64/openmpi3/lib/libmpi.so
        -- MPI Executable:       /usr/lib64/openmpi3/bin/mpiexec
        -- MPI Num Proc Flag:    -n
        -- Found DTCMP: /root/mpifileutils_src/install/lib/libdtcmp.so
        -- Found LibArchive: /root/mpifileutils_src/install/lib/libarchive.so (Required is at least version "3.5.0")
        -- Found CART: /root/daos_src/daos/install/lib64/libcart.so
        /root/daos_src/daos/install/include
        -- Found DAOS: /root/daos_src/daos/install/lib64/libdaos.so
        -- Found LibCircle: /root/mpifileutils_src/install/lib/libcircle.so
        -- Found BZip2: /usr/lib64/libbz2.so (found version "1.0.6")
        -- Looking for BZ2_bzCompressInit
        -- Looking for BZ2_bzCompressInit - found
        -- Could NOT find LibCap (missing: LibCap_LIBRARIES LibCap_INCLUDE_DIRS)
        -- Found OpenSSL: /usr/lib64/libcrypto.so (found version "1.0.2k")
        -- Configuring done
        -- Generating done
        -- Build files have been written to: /root/mpifileutils_src/build
        [root@ssc-vm-2051 build]#

* Make install

    ```make install```
    
        Terminal logs -

        :/root/daos_src/daos/install/lib64"
        -- Installing: /root/mpifileutils_src/install/bin/dreln
        -- Set runtime path of "/root/mpifileutils_src/install/bin/dreln" to "/root/mpifileutils_src/install/lib64:/usr/lib64/openmpi3/lib:/root/mpifileutils_src/install/lib:/root/daos_src/daos/install/lib64"
        -- Installing: /root/mpifileutils_src/install/bin/drm
        -- Set runtime path of "/root/mpifileutils_src/install/bin/drm" to "/root/mpifileutils_src/install/lib64:/usr/lib64/openmpi3/lib:/root/mpifileutils_src/install/lib:/root/daos_src/daos/install/lib64"
        -- Installing: /root/mpifileutils_src/install/bin/dstripe
        -- Set runtime path of "/root/mpifileutils_src/install/bin/dstripe" to "/root/mpifileutils_src/install/lib64:/usr/lib64/openmpi3/lib:/root/mpifileutils_src/install/lib:/root/daos_src/daos/install/lib64"
        -- Installing: /root/mpifileutils_src/install/bin/dsync
        -- Set runtime path of "/root/mpifileutils_src/install/bin/dsync" to "/root/mpifileutils_src/install/lib64:/usr/lib64/openmpi3/lib:/root/mpifileutils_src/install/lib:/root/daos_src/daos/install/lib64"
        -- Installing: /root/mpifileutils_src/install/bin/dwalk
        -- Set runtime path of "/root/mpifileutils_src/install/bin/dwalk" to "/root/mpifileutils_src/install/lib64:/usr/lib64/openmpi3/lib:/root/mpifileutils_src/install/lib:/root/daos_src/daos/install/lib64"
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dbcast.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dchmod.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dcmp.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dcp.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/ddup.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dbz2.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dfind.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dreln.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/drm.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dstripe.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dsync.1
        -- Installing: /root/mpifileutils_src/install/share/man/man1/dwalk.1
        [root@ssc-vm-2051 build]#


# Object copy using mpifileutils

* Create two empty POSIX containers using these steps[https://github.com/Seagate/cortx-experiments/blob/main/daos%2Bcortx/docs/setup_daos.md#start-agent]

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

            [root@ssc-vm-2051 daos]# export pool1=c7b0c9e2-028d-4dde-b016-a68743dba49a


    - Container 1 creation & export
        
        Terminal logs -

            [root@ssc-vm-2051 daos]# daos container create --pool=$pool1 --path=/tmp/cont1 --type=POSIX
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
            [root@ssc-vm-2051 daos]#

            [root@ssc-vm-2051 daos]# export cont1=226b4ee3-c972-4fea-8619-82f30e5bec4b

    - Container 2 creation & export
    
            Terminal logs -

            [root@ssc-vm-2051 daos]# daos container create --pool=$pool1 --path=/tmp/cont2 --type=POSIX
            fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
            fi   WARN src/gurt/fault_inject.c:724 d_fault_attr_set() Fault Injection attr not set feature not included in build
            daos INFO src/client/api/job.c:89 dc_job_init() Using JOBID ENV: DAOS_JOBID
            daos INFO src/client/api/job.c:90 dc_job_init() Using JOBID ssc-vm-2051.colo.seagate.com-6666
            mgmt INFO src/mgmt/cli_mgmt.c:360 dc_mgmt_net_cfg() Using client provided OFI_INTERFACE: lo
            crt  INFO src/cart/crt_init.c:311 crt_init_opt() libcart version 4.9.0 initializing
            fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
            crt  WARN src/cart/crt_init.c:162 data_init() FI_UNIVERSE_SIZE was not set; setting to 2048
            client INFO src/utils/daos.c:168 cmd_args_print()       DAOS system name: daos_server
            client INFO src/utils/daos.c:169 cmd_args_print()       pool UUID: c7b0c9e2-028d-4dde-b016-a68743dba49a
            client INFO src/utils/daos.c:170 cmd_args_print()       cont UUID: 00000000-0000-0000-0000-000000000000
            client INFO src/utils/daos.c:174 cmd_args_print()       pool svc: parsed 0 ranks from input NULL
            client INFO src/utils/daos.c:178 cmd_args_print()       attr: name=NULL, value=NULL
            client INFO src/utils/daos.c:182 cmd_args_print()       path=/tmp/cont2, type=POSIX, oclass=UNKNOWN, chunk_size=0
            client INFO src/utils/daos.c:188 cmd_args_print()       snapshot: name=NULL, epoch=0, epoch range=NULL (0-0)
            client INFO src/utils/daos.c:189 cmd_args_print()       oid: 0.0
            Successfully created container bcd454f5-fef6-4705-8495-77d2b918c5da type POSIX
            fi   WARN src/gurt/fault_inject.c:693 d_fault_inject_fini() Fault Injection not finalized feature not included in build
            fi   WARN src/gurt/fault_inject.c:693 d_fault_inject_fini() Fault Injection not finalized feature not included in build
            [root@ssc-vm-2051 daos]#
            
            [root@ssc-vm-2051 daos]# export cont2=bcd454f5-fef6-4705-8495-77d2b918c5da


# Mount cotainer using dfuse

* Create new directories to mount containers

    ```mkdir /mnt/rajkumar/cont1```
    
    ```mkdir /mnt/rajkumar/cont2```

* Mount containers

    ```dfuse -m /mnt/rajkumar/cont1 --pool $pool --cont $cont1```

        [root@ssc-vm-2051 daos]# dfuse -m /mnt/rajkumar/cont1 --pool $pool --cont $cont1
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

    ```dfuse -m /mnt/rajkumar/cont2 --pool $pool --cont $cont2```

        [root@ssc-vm-2051 daos]# dfuse -m /mnt/rajkumar/cont2 --pool $pool --cont $cont2
        fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
        fi   WARN src/gurt/fault_inject.c:724 d_fault_attr_set() Fault Injection attr not set feature not included in build
        daos INFO src/client/api/job.c:89 dc_job_init() Using JOBID ENV: DAOS_JOBID
        daos INFO src/client/api/job.c:90 dc_job_init() Using JOBID ssc-vm-2051.colo.seagate.com-7284
        mgmt INFO src/mgmt/cli_mgmt.c:360 dc_mgmt_net_cfg() Using client provided OFI_INTERFACE: lo
        crt  INFO src/cart/crt_init.c:311 crt_init_opt() libcart version 4.9.0 initializing
        fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
        crt  WARN src/cart/crt_init.c:162 data_init() FI_UNIVERSE_SIZE was not set; setting to 2048
        duns INFO src/client/dfs/duns.c:393 duns_resolve_path() Path does not represent a DAOS link
        dfuse INFO src/client/dfuse/dfuse_main.c:457 main(0xa98000) duns_resolve_path() returned 61 No data available
        dfuse INFO src/client/dfuse/dfuse_main.c:60 dfuse_send_to_fg() Sending 0 to fg

* craete objects (files) inside container


    ```cd /mnt/rajkumar/cont1```
        
    ```touch fileA fileB```
        
     Checking contents of both container -
        
        [root@ssc-vm-2051 cont1]# ls
        fileA  fileB
        
        [root@ssc-vm-2051 cont1]# cd /mnt/rajkumar/cont2
        [root@ssc-vm-2051 cont2]# ls
        [root@ssc-vm-2051 cont2]#


* Object copy

    For object copy within a pool and between containers dcp command is used to showcase the operation.

    ```mpirun -np 1 --allow-run-as-root /root/mpifileutils_src/install/bin/dcp -v --daos-src-pool $pool1 --daos-src-cont $cont1 --daos-dst-pool $pool1 --daos-dst-cont $cont2```

    make sure openmpi commands (mpicc, mpirun) are already added in path and eccessible.
    
    In this example mpifileutils' source is in /root/mpifileutils_src/ directory. One should use <path/to/mpifileutils/source>/install/bin/dcp.

        Terminal logs -
        
        [root@ssc-vm-2051 cont2]# mpirun -np 1 --allow-run-as-root /root/mpifileutils_src/install/bin/dcp -v --daos-src-pool $pool --daos-src-cont $cont1 --daos-dst-pool $pool --daos-dst-cont $cont2
        01/19-00:49:06.63 ssc-vm-2051 DAOS[7782/7782] fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
        01/19-00:49:06.63 ssc-vm-2051 DAOS[7782/7782] fi   WARN src/gurt/fault_inject.c:724 d_fault_attr_set() Fault Injection attr not set feature not included in build
        01/19-00:49:06.64 ssc-vm-2051 DAOS[7782/7782] daos INFO src/client/api/job.c:89 dc_job_init() Using JOBID ENV: DAOS_JOBID
        01/19-00:49:06.64 ssc-vm-2051 DAOS[7782/7782] daos INFO src/client/api/job.c:90 dc_job_init() Using JOBID ssc-vm-2051.colo.seagate.com-7782
        01/19-00:49:06.65 ssc-vm-2051 DAOS[7782/7782] mgmt INFO src/mgmt/cli_mgmt.c:360 dc_mgmt_net_cfg() Using client provided OFI_INTERFACE: lo
        01/19-00:49:06.65 ssc-vm-2051 DAOS[7782/7782] crt  INFO src/cart/crt_init.c:311 crt_init_opt() libcart version 4.9.0 initializing
        01/19-00:49:06.65 ssc-vm-2051 DAOS[7782/7782] fi   WARN src/gurt/fault_inject.c:687 d_fault_inject_init() Fault Injection not initialized feature not included in build
        01/19-00:49:06.65 ssc-vm-2051 DAOS[7782/7782] crt  WARN src/cart/crt_init.c:162 data_init() FI_UNIVERSE_SIZE was not set; setting to 2048
        [2021-01-19T00:49:09] Successfully copied to DAOS Destination Container.
        01/19-00:49:09.93 ssc-vm-2051 DAOS[7782/7782] fi   WARN src/gurt/fault_inject.c:693 d_fault_inject_fini() Fault Injection not finalized feature not included in build
        01/19-00:49:09.93 ssc-vm-2051 DAOS[7782/7782] fi   WARN src/gurt/fault_inject.c:693 d_fault_inject_fini() Fault Injection not finalized feature not included in build
        [root@ssc-vm-2051 cont2]#

    To verify -
        
        [root@ssc-vm-2051 cont2]# cd /mnt/rajkumar/cont2
        [root@ssc-vm-2051 cont2]# ls
        fileA  fileB
        [root@ssc-vm-2051 cont2]#

This clearly demonstrate that 2 file objects which were part of POSIX type container 1 (source) are copied to POSIX type container 2(destinaltion) using mpifileutils and that too within a single pool.
