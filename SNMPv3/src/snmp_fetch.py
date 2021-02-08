#! /bin/python
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           UsmUserData('sumedh_sha_aes', 'authpass', 'privpass',
			authProtocol=usmHMACSHAAuthProtocol,
			privProtocol=usmAesCfb128Protocol),
	   UdpTransportTarget(('10.230.250.57', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0))
	   )
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))