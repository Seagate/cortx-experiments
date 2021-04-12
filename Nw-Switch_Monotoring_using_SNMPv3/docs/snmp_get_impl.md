# Get managment information from the Agent

## Configuration on Mellanox Switch

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

## Configuration on the Manager Server
### Queries using Net-Snmp command-line interface
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
### Queries Using a python script
1. Install pysnmp module
   ```bash
   pip3 install pysnmp
   ```
1. Use commands like getCmd or nextCmd provided by pysnmp.hlapi to get values from the agent.

   The v3 user can be configured using UsmUserData() object.

   The agent ip:port can be configured using UdpTransportTarget() object.

   Oid or Mib id to get value can be set using ObjectTyp() object.

   Sample scripts :
   * [snmp_fetch.py](../src/snmp_fetch.py)
   * [snmp_walk.py](../src/snmp_walk.py)

