# Testing v3 Traps/Informs
## Configuration on the Manager Server
### Using Net-Snmp rpms
1. Stop snmptrapd.service if running
   ```bash
   >> systemctl stop snmptrapd
   ```
1. Add following lines in /etc/snmp/snmptrad.conf
   ```bash
   >> createUser inform_sender SHA authpass AES privpass
 
   >> authUser log,execute inform_sender
   ##  save the file and exit
   ```
1. Note the engineid from last lin of the file `/var/lib/net-snmp/snmpd.conf`
   ```
   oldEngineID 0x80001f8880493087620edd1a5f00000000
   ```
1. Start the snmptrad.service again.
   ```bash
   >> systemctl start snmptrapd
   ```
### Using python script
1. Ensure that Python module `pysnmp` is installed.
1. Refer the script : [trap_reciver.py](https://github.com/sumedhak27/cortx-experiments/blob/EOS-11060-Mellanox_SN2100_monitoring_using_SNMPv3/SNMPv3/src/trap_receiver.py) or [Pysnmp documentation](https://pysnmp.readthedocs.io/en/latest/) to write a script.
1. Edit or add the appropriate credentials for :
   1. ip and port script is listening to
   1. v3 user credentials
1. The Manger Server is ready to accept any trap/inform message

## Configuration on Mellanox Switch
1. Add the user registered on Manager as an inform destination. engine-id can be found in `/var/lib/net-snmp/snmpd.conf` file after creation of v3 user.
   ```bash
   >> net add snmp-server trap-destination 10.230.242.110 username infom_sender \
   auth-sha authpass encrypt-aes privpass engine-id 0x80001f8880ec70e17424be1f5f00000000 inform

   ## username , passphrase and engine-id should be as mentioned as it is configured on the server and it should 
   ## match with user config on server
   ```
1. Enable different traps as required
   ```bash
   >> net add snmp-server trap-link-up check-frequency 15

   >> net add snmp-server trap-link-down check-frequency 10

   >> net add snmp-server trap-snmp-auth-failures

   >> net add snmp-server trap-cpu-load-average one-minute 4.34 five-minute 2.32 fifteen-minute 6.5

   >> net commit

   Other types of traps are supported by net-snmp and can be enabled by editing the snmpd.conf file
   ##All the following commands are to be placed inside the snmpd.conf file

   SNMPv3 needs internal v3 user with appropriate permissions to internally query necessary information

   >> createuser internaluser
   >> iquerysecname internaluser
   >> rouser internaluser
   commands that set different trap triggers :

   5. Generate alert if any cpu core usage exceeds 90%

   >> monitor -r 60 "VM CPU Load Too High" hrProcessorLoad > 90
   6. Generate alert when the 1 minute, 5 minute and 15 minute load averages exceed a certain amount

   >> load 12 10 5

   >> monitor -r 60 -o laNames -o laErrMessage "Load Average Exceeded" laErrorFlag != 0
   7. Generate alert when the free space on the folders to be monitored fall below the minimum space required.

   >> disk /var/log 10% 
   #OR 
   >> includeAllDisks 5%
 
   >> monitor -r 60 -o dskErrorMsg "Folder HDD Space Low" dskErrorFlag != 0
   8. Generate alert when VM RAM used exceeds X KB. e.g. 4 GB = 4194304 KB

   >> monitor -r 60 -I "VM RAM Usage Too High" hrStorageUsed.1 > 4194304
   9. Generate alert when any process memory usage exceeds X KB, e.g. 1 GB = 1048576 KB

   >> monitor -r 60 -o hrSWRunName -o hrSWRunPath "Process RAM Usage Too High" hrSWRunPerfMem > 1048576
   ```