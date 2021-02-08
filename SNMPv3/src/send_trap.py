#! /bin/python
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    sendNotification(
        SnmpEngine(),
	    UsmUserData('inform_sender','authpass','privpass',
		        authProtocol=usmHMACSHAAuthProtocol,
                privProtocol=usmAesCfb128Protocol),        
	    UdpTransportTarget(('10.230.242.110', 162)),
        ContextData(),
        'inform',
	    NotificationType(
            ObjectIdentity('SNMPv2-MIB', 'coldStart')
        ).addVarBinds(
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0), 'my system')
        )
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