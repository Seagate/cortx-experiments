#! /bin/python
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine(v2c.OctetString(hexValue='80001f8880ec70e17424be1f5f00000000'))

# Transport setup

# UDP over IPv4
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('10.230.242.110', 162))
)

config.addV1System(snmpEngine, 'mynetwork', 'public')

# SNMPv3/USM setup
# user: usr-sha-aes128, auth: SHA, priv AES, securityEngineId: 8000000001020304
# this USM entry is used for TRAP receiving purpose
config.addV3User(snmpEngine, 'testuser',
	config.usmHMACSHAAuthProtocol, 'authtest',
	config.usmAesCfb128Protocol, 'privtest',
)

# config.addV3User(
#    snmpEngine, 'inform_sender',
#    config.usmHMACSHAAuthProtocol, 'authpass',
#    config.usmAesCfb128Protocol, 'privpass',
#    securityEngineId=v2c.OctetString(hexValue='80001f8880ec70e17424be1f5f00000000')
#)

config.addV3User(
    snmpEngine, 'sumedhak',
    config.usmHMACMD5AuthProtocol, 'mysecretauth',
    config.usmDESPrivProtocol, 'mysecretpriv'
)

config.addV3User(snmpEngine, 'inform_sender', 
    config.usmHMACSHAAuthProtocol, 'authpass',
    config.usmAesCfb128Protocol, 'privpass',
)

# Callback function for receiving notifications
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
          varBinds, cbCtx):
    print('Notification from ContextEngineId "%s", ContextName "%s"' %
            (contextEngineId.prettyPrint(), contextName.prettyPrint()))
            
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# Register SNMP Application at the SNMP engine
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1)  # this job would never finish

# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise        