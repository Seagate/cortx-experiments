# SNMPv3 Experiments
Simple Network Management Protocol (SNMP) is an Internet Standard protocol for collecting and organizing information about managed devices on IP networks and for monitoring or modifying that information to change device behavior.

## SNMP Architechture
In typical uses of SNMP, one or more administrative computers called managers have the task of monitoring or managing a group of hosts or devices on a computer network. Each managed system executes a software component called an agent which reports information via SNMP to the manager.

SNMP-managed network consists of three key components:
* Managed devices   - any networking device like router, switch, hub, power supply unit, etc.
* Agent – software which runs on managed devices
* Network management station (NMS) – software that runs on the manager
<img src="https://github.com/sumedhak27/cortx-experiments/blob/EOS-11060-Mellanox_SN2100_monitoring_using_SNMPv3/SNMPv3/docs/Snmp_architechture.png?raw=true" alt="Architecture Diagram" width="65%">

### Resources used 
* Linux Virtual machines :
   * ssc-vm-0748.colo.seagate.com (Agent)
   * ssc-vm-0804.colo.seagate.com (Manager)
* Mellanox SN2100 network switch  (Agent)
* Software Packages :
   * [Net-Snmp rpms](http://www.net-snmp.org/)  For Linux or windows machines

     **OR**
   * [pysnmp module](https://pypi.org/project/pysnmp/) For writing python Scripts or Application



## Get information from the Agent

### Configuration on Mellanox Switch

>NOTE: Mellanox switches run with Cumulus Linux operating system which is already enabled with SNMP capabilities and it can be configured via using cumulus linux commands (recommended) or by editing the /etc/snmp/snmpd.conf file. 

1. Add the IP address of the manager server to the config,
   ```bash
   >> net add snmp-server listening-address 10.230.242.110
   ```
1. Create a v3 user which can query the agent.
   ```bash
   >> net add snmp-server username cumulusro auth-sha seagate1 encrypt-aes encryptseagate1   
   ## username and passphrases can be changed
   ```
1. Assign required oid permission level to the user.
   ```bash
   >> net add snmp-server username cumulusro auth-sha seagate1 encrypt-aes encryptseagate1 oid .1
   ## username and passphrases should be same as that of configured in previous command
   ```
4. Commit the changes.
   ```bash
   >> net commit
   ```

### Configuration on the Manager Server
#### Queries using Net-Snmp command-line interface
1. Install Net-snmp rpms
   ```bash
   >> sudo yum install net-snmp net-snmp-libs net-snmp-utils -y
   ```
1. Start the snmpd.service
   ```bash
   >> systemctl start snmpd
   ```
1. Check/Set firewall rule
   ```bash
   ## check if firewalld is running or not 
   >> systemctl status firewall
 
   ## if it is running then run 2 commands mentioned below else skip these commands
 
   >> firewall-cmd --permanent --zone=public --add-port={161/udp,162/udp}
 
   >> firewall-cmd --reload
   ```
1. Now We can Query any value from enabled MIBS.
   Here are some examples :
   ```bash
   >> snmpget -v3 -u cumulusro -a SHA -A seagate1 -x AES -X encryptseagate1 -l authPriv 10.237.66.62 sysDescr.0
   SNMPv2-MIB::sysDescr.0 = STRING: Cumulus Linux 3.7.10 (Linux Kernel 4.1.33-1+cl3u24)
   
   >> snmpwalk -v3 -u cumulusro -a SHA -A seagate1 -x AES -X encryptseagate1 -l authPriv 
   10.237.66.62 interfaces
   IF-MIB::ifNumber.0 = INTEGER: 37
   IF-MIB::ifIndex.1 = INTEGER: 1
   IF-MIB::ifIndex.2 = INTEGER: 2
   IF-MIB::ifIndex.3 = INTEGER: 3
   IF-MIB::ifIndex.4 = INTEGER: 4
   IF-MIB::ifIndex.17 = INTEGER: 17
   IF-MIB::ifIndex.18 = INTEGER: 18
   IF-MIB::ifIndex.19 = INTEGER: 19
   IF-MIB::ifIndex.20 = INTEGER: 20
   IF-MIB::ifIndex.21 = INTEGER: 21
   IF-MIB::ifIndex.22 = INTEGER: 22
   IF-MIB::ifIndex.23 = INTEGER: 23
   IF-MIB::ifIndex.24 = INTEGER: 24
   IF-MIB::ifIndex.25 = INTEGER: 25
   .
   .  .  .  .  .  .  .  .  .  .  .  .
   ## full output in interfacewalk.txt file attached
   ```
#### Queries Using a python script
1. Install pysnmp module
   ```bash
   pip3 install pysnmp
   ```
1. Use commands like getCmd or nextCmd provided by pysnmp.hlapi to get values from the agent.

   The v3 user can be configured using UsmUserData() object.

   The agent ip:port can be configured using UdpTransportTarget() object.

   Oid or Mib id to get value can be set using ObjectTyp() object.

   Sample scripts :
   * [snmp_fetch.py](https://github.com/sumedhak27/cortx-experiments/blob/EOS-11060-Mellanox_SN2100_monitoring_using_SNMPv3/SNMPv3/src/snmp_fetch.py)
   * [snmp_walk.py](https://github.com/sumedhak27/cortx-experiments/blob/EOS-11060-Mellanox_SN2100_monitoring_using_SNMPv3/SNMPv3/src/snmp_walk.py)


## Testing v3 Traps/Informs
### Configuration on the Manager Server
#### Using Net-Snmp rpms
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
#### Using python script
1. Ensure that Python module `pysnmp` is installed.
1. Refer the script : [trap_reciver.py](https://github.com/sumedhak27/cortx-experiments/blob/EOS-11060-Mellanox_SN2100_monitoring_using_SNMPv3/SNMPv3/src/trap_receiver.py) or [Pysnmp documentation](https://pysnmp.readthedocs.io/en/latest/) to write a script.
1. Edit or add the appropriate credentials for :
   1. ip and port script is listening to
   1. v3 user credentials
1. The Manger Server is ready to accept any trap/inform message

### Configuration on Mellanox Switch
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
