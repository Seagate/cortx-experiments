#! /bin/python

from pysnmp.hlapi import *

for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in nextCmd(SnmpEngine(),
            UsmUserData('sumedh_sha_aes', 'authpass', 'privpass',
                authProtocol=usmHMACSHAAuthProtocol,
                privProtocol=usmAesCfb128Protocol),
                UdpTransportTarget(('10.230.250.57', 161)),
                ContextData(),
                ObjectType(ObjectIdentity('IF-MIB'))):

    if errorIndication:
        print(errorIndication)
        break
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        break
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
