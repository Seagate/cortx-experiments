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



## Enable Get/Set of values on Agent for the Manager

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
   ```
   >> net commit
   ```

### Configuration on the Manager Server
#### Queries using Net-Snmp command-line interface
1. Install Net-snmp rpms
   ```
   >> sudo yum install net-snmp net-snmp-libs net-snmp-utils -y
   ```
1. Start the snmpd.service
   ```
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


