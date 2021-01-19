# Pre-requisites

* cmake version 3.1 or more required.

    ```yum install cmake3```
        
        To Verify -
        
        ```cmake3 --version```
        
        Terminal logs -
        
        [root@ssc-vm-2051 daos]# cmake3 --version
        cmake3 version 3.17.5

        CMake suite maintained and supported by Kitware (kitware.com/cmake).

* Install openmpi

    ```yum install openmpi```

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

        To verify --
        
        ``` mpicc``` 7 ```which mpicc```
        
        Terminal logs -
        
        [root@ssc-vm-2051 daos]# mpicc
        gcc: fatal error: no input files

        [root@ssc-vm-2051 daos]# which mpicc
        /usr/lib64/openmpi3/bin/mpicc

# Install dependencies

* Make a directory for your setup

    ```mkdir mpifileutils_src```

* Create a build script

    ```touch build_deps.sh```
    
    - To get the latest contents for buuld script, kindly checkout mpifileutil's github-repo[https://github.com/hpc/mpifileutils/blob/master/doc/rst/build.rst]
    
    - Copy contents from above locations to build scripts.
    
            Sample build scripts is presented here[] //TODO

*  Run build script

    ```sh build_deps.sh```

        Terminal logs -
        
        libtool: install: /bin/install -c .libs/libdtcmp.so /root/mpifileutils_src/install/lib/libdtcmp.so
        libtool: install: /bin/install -c .libs/libdtcmp.lai /root/mpifileutils_src/install/lib/libdtcmp.la
        libtool: install: /bin/install -c .libs/libdtcmp.a /root/mpifileutils_src/install/lib/libdtcmp.a
        libtool: install: chmod 644 /root/mpifileutils_src/install/lib/libdtcmp.a
        libtool: install: ranlib /root/mpifileutils_src/install/lib/libdtcmp.a
        libtool: finish: PATH="/usr/lib64/openmpi3/bin/:/root/daos_src/daos/install/bin/:/root/daos_src/daos/install/sbin:/usr/local/sbin:/sbin:/bin:/usr/sbin:/usr/bin:/opt/puppetlabs/bin:/root/bin:/sbin" ldconfig -n /root/mpifileutils_src/install/lib
        ----------------------------------------------------------------------
        Libraries have been installed in:
           /root/mpifileutils_src/install/lib

        If you ever happen to want to link against installed libraries
        in a given directory, LIBDIR, you must either use libtool, and
        specify the full pathname of the library, or use the `-LLIBDIR'
        flag during linking and do at least one of the following:
           - add LIBDIR to the `LD_LIBRARY_PATH' environment variable
             during execution
           - add LIBDIR to the `LD_RUN_PATH' environment variable
             during linking
           - use the `-Wl,-rpath -Wl,LIBDIR' linker flag
           - have your system administrator add LIBDIR to `/etc/ld.so.conf'

        See any operating system documentation about shared libraries for
        more information, such as the ld(1) and ld.so(8) manual pages.
        ----------------------------------------------------------------------
         /bin/mkdir -p '/root/mpifileutils_src/install/include'
         /bin/install -c -m 644 dtcmp.h '/root/mpifileutils_src/install/include'
        make[2]: Leaving directory `/root/mpifileutils_src/deps/dtcmp-1.1.0/src'
        make[1]: Leaving directory `/root/mpifileutils_src/deps/dtcmp-1.1.0/src'
        make[1]: Entering directory `/root/mpifileutils_src/deps/dtcmp-1.1.0'
        make[2]: Entering directory `/root/mpifileutils_src/deps/dtcmp-1.1.0'
        make[2]: Nothing to be done for `install-exec-am'.
         /bin/mkdir -p '/root/mpifileutils_src/install/share/dtcmp'
         /bin/install -c -m 644 README LICENSE.TXT '/root/mpifileutils_src/install/share/dtcmp'
         /bin/mkdir -p '/root/mpifileutils_src/install/lib/pkgconfig'
         /bin/install -c -m 644 libdtcmp.pc '/root/mpifileutils_src/install/lib/pkgconfig'
        make[2]: Leaving directory `/root/mpifileutils_src/deps/dtcmp-1.1.0'
        make[1]: Leaving directory `/root/mpifileutils_src/deps/dtcmp-1.1.0'


# Clone source

    build latest mpiFileUtils from the master branch with DAOS Support

    ```git clone https://github.com/hpc/mpifileutils```

    ```mkdir build```

    ```cd build```

    ```cmake3 ../mpifileutils -DWITH_DTCMP_PREFIX=../install -DWITH_LibCircle_PREFIX=../install -DWITH_CART_PREFIX=/root/src_daos/daos/install -DWITH_DAOS_PREFIX=/root/src_daos/daos/install -DCMAKE_INSTALL_PREFIX=../install -DENABLE_DAOS=ON```

        Terminal logs -
        
        -- MPI Executable:       /usr/lib64/openmpi3/bin/mpiexec
        -- MPI Num Proc Flag:    -n
        -- Found DTCMP: /root/mpifileutils_src/install/lib/libdtcmp.so
        CMake Error at /usr/share/cmake3/Modules/FindPackageHandleStandardArgs.cmake:164 (message):
          Could NOT find LibArchive (missing: LibArchive_LIBRARIES
          LibArchive_INCLUDE_DIRS) (Required is at least version "3.5.0")
        Call Stack (most recent call first):
          /usr/share/cmake3/Modules/FindPackageHandleStandardArgs.cmake:445 (_FPHSA_FAILURE_MESSAGE)
          cmake/FindLibArchive.cmake:22 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
          CMakeLists.txt:87 (FIND_PACKAGE)


        -- Configuring incomplete, errors occurred!
        See also "/root/mpifileutils_src/build/CMakeFiles/CMakeOutput.log".
        [root@ssc-vm-2051 build]#


PATH=/home/737530/integration/cmake-3.6.2/Utilities/cmlibarchive/libarchive:$PATH

yum install libarchive-devel.x86_64


path related issues in command

yum install cart-devel.x86_64

-- MPI CXX Libraries:     /usr/lib64/openmpi3/lib/libmpi_cxx.so;/usr/lib64/openmpi3/lib/libmpi.so
-- MPI Executable:       /usr/lib64/openmpi3/bin/mpiexec
-- MPI Num Proc Flag:    -n
-- Found LibArchive: /usr/lib64/libarchive.so (Required is at least version "3.5.0")
CMake Error at /usr/share/cmake3/Modules/FindPackageHandleStandardArgs.cmake:164 (message):
  Could NOT find CART (missing: CART_LIBRARIES CART_INCLUDE_DIRS)
Call Stack (most recent call first):
  /usr/share/cmake3/Modules/FindPackageHandleStandardArgs.cmake:445 (_FPHSA_FAILURE_MESSAGE)
  cmake/FindCART.cmake:28 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  CMakeLists.txt:94 (FIND_PACKAGE)

yum install bzip2

bzip2-1.0.6-13.el7.x86_64.rpm                                                                                                         |  52 kB  00:00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : bzip2-1.0.6-13.el7.x86_64                                                                                                                 1/1
Loaded plugins: fastestmirror, product-id, subscription-manager
  Verifying  : bzip2-1.0.6-13.el7.x86_64                                                                                                                 1/1

Installed:
  bzip2.x86_64 0:1.0.6-13.el7

Complete!
[root@ssc-vm-2051 build]#

[root@ssc-vm-2051 build]# which bzip2
/bin/bzip2



error :

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


-- Configuring incomplete, errors occurred!
See also "/root/mpifileutils_src/build/CMakeFiles/CMakeOutput.log".
[root@ssc-vm-2051 build]#


yum install bzip2-devel.x86_64


Installed size: 382 k
Is this ok [y/d/N]: y
Downloading packages:
bzip2-devel-1.0.6-13.el7.x86_64.rpm                                                                                                   | 218 kB  00:00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : bzip2-devel-1.0.6-13.el7.x86_64                                                                                                           1/1
Loaded plugins: fastestmirror, product-id, subscription-manager
  Verifying  : bzip2-devel-1.0.6-13.el7.x86_64                                                                                                           1/1

Installed:
  bzip2-devel.x86_64 0:1.0.6-13.el7

Complete!
[root@ssc-vm-2051 build]#
[0] < 1:root@ssc-vm-2051:~/daos_src/daos  2:root@ssc-vm-2051:/mnt/daos- 3:root@ssc-vm-2051:~/mp

SUCCEED

[root@ssc-vm-2051 build]#  cmake3 ../mpifileutils -DWITH_DTCMP_PREFIX=../install -DWITH_LibCircle_PREFIX=../install -DWITH_CART_PREFIX=/root/daos_src/daos/install -DWITH_DAOS_PREFIX=/root/daos_src/daos/install -DCMAKE_INSTALL_PREFIX=../install -DENABLE_DAOS=ON
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
/root/daos_src/daos/install/include
-- Found BZip2: /usr/lib64/libbz2.so (found version "1.0.6")
-- Looking for BZ2_bzCompressInit
-- Looking for BZ2_bzCompressInit - found
-- Could NOT find LibCap (missing: LibCap_LIBRARIES LibCap_INCLUDE_DIRS)
-- Found OpenSSL: /usr/lib64/libcrypto.so (found version "1.0.2k")
-- Configuring done
-- Generating done
-- Build files have been written to: /root/mpifileutils_src/build
[root@ssc-vm-2051 build]#


------------------------- after pr 436 and new build deps -------------------------------------

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


git clone --depth 1 https://github.com/hpc/mpifileutils
   mkdir build install
   cd build
   cmake ../mpifileutils \
     -DWITH_DTCMP_PREFIX=../install \
     -DWITH_LibCircle_PREFIX=../install \
     -DCMAKE_INSTALL_PREFIX=../install \
     -DWITH_CART_PREFIX=</path/to/daos/> \
     -DWITH_DAOS_PREFIX=</path/to/daos/> \
     -DENABLE_DAOS=ON
   make install
   
   
   [root@ssc-vm-2051 mpifileutils_src]# git clone --depth 1 https://github.com/hpc/mpifileutils
Cloning into 'mpifileutils'...
remote: Enumerating objects: 243, done.
remote: Counting objects: 100% (243/243), done.
remote: Compressing objects: 100% (202/202), done.
remote: Total 243 (delta 37), reused 109 (delta 11), pack-reused 0
Receiving objects: 100% (243/243), 430.01 KiB | 0 bytes/s, done.
Resolving deltas: 100% (37/37), done.
[root@ssc-vm-2051 mpifileutils_src]# cd mpifileutils/
[root@ssc-vm-2051 mpifileutils]# ls



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


make install

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


------------------------------------------------------------------------------------------------------



[root@ssc-vm-2051 daos]#
[root@ssc-vm-2051 daos]# daos container create --pool=$pool --path=/tmp/cont2 --type=POSIX
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
[root@ssc-vm-2051 daos]#


/tmp/cont1 226b4ee3-c972-4fea-8619-82f30e5bec4b
/tmp/cont2 bcd454f5-fef6-4705-8495-77d2b918c5da
pool c7b0c9e2-028d-4dde-b016-a68743dba49a


export cont1 cont2 pool


mkdir /mnt/rajkumar/cont1
mkdir /mnt/rajkumar/cont2

dfuse -m /mnt/rajkumar/cont1 --pool $pool --cont $cont1

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

dfuse -m /mnt/rajkumar/cont2 --pool $pool --cont $cont2

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


[root@ssc-vm-2051 daos]# cd /mnt/rajkumar/cont1
[root@ssc-vm-2051 cont1]# ls
[root@ssc-vm-2051 cont1]#
[root@ssc-vm-2051 cont1]# touch fileA fileB
[root@ssc-vm-2051 cont1]# ls
fileA  fileB
[root@ssc-vm-2051 cont1]# cd /mnt/rajkumar/cont2
[root@ssc-vm-2051 cont2]# ls
[root@ssc-vm-2051 cont2]#


mpirun -np 3 --allow-run-as-root /root/mpifileutils_src/install/bin/dcp -v --daos-src-pool $pool --daos-src-cont $cont1 --daos-dst-pool $pool --daos-dst-cont $cont2

[root@ssc-vm-2051 cont2]# PATH=/usr/lib64/openmpi3/bin/:$PATH

[root@ssc-vm-2051 cont2]# mpirun -np 3 --allow-run-as-root /root/mpifileutils_src/install/bin/dcp -v --daos-src-pool $pool --daos-src-cont $cont1 --daos-dst-pool $pool --daos-dst-cont $cont2
--------------------------------------------------------------------------
There are not enough slots available in the system to satisfy the 3 slots
that were requested by the application:
  /root/mpifileutils_src/install/bin/dcp

Either request fewer slots for your application, or make more slots available
for use.
--------------------------------------------------------------------------
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


[root@ssc-vm-2051 cont2]# cd /mnt/rajkumar/cont2
[root@ssc-vm-2051 cont2]# ls
fileA  fileB
[root@ssc-vm-2051 cont2]#
