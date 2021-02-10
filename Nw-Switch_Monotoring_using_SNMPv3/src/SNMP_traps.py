"""
 ****************************************************************************
 Filename:          SNMP_Traps.py
 Description:       Catches SNMP traps, determines PDU or Switch and
                    notifies the appropriate trap msg handler.
 Creation Date:     3/08/2016
 Author:            Jake Abernathy
 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""
import json

from framework.base.module_thread import SensorThread
from framework.base.internal_msgQ import InternalMsgQ
from framework.utils.service_logging import logger

# Modules that receive messages from this module
from framework.rabbitmq.rabbitmq_egress_processor import RabbitMQegressProcessor
from message_handlers.logging_msg_handler import LoggingMsgHandler

from json_msgs.messages.sensors.snmp_trap import SNMPtrapMsg

import pysnmp
import pyasn1
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp, udp6
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c
from pysnmp.smi import builder, view, compiler

from zope.interface import implementer
from sensors.INode_data import INodeData

@implementer(INodeData)
class SNMPtraps(SensorThread, InternalMsgQ):

    SENSOR_NAME       = "SNMPtraps"
    PRIORITY          = 1

    # Section and keys in configuration file
    SNMPTRAPS         = SENSOR_NAME.upper()
    ENABLED_TRAPS     = 'enabled_traps'
    BIND_IP           = 'bind_ip'
    BIND_PORT         = 'bind_port'
    ENABLED_MIBS      = 'enabled_MIBS'


    @staticmethod
    def name():
        """@return: name of the monitoring module."""
        return SNMPtraps.SENSOR_NAME

    def __init__(self):
        super(SNMPtraps, self).__init__(self.SENSOR_NAME, self.PRIORITY)
        self._latest_trap = {}

    def initialize(self, conf_reader, msgQlist, product):
        """initialize configuration reader and internal msg queues"""

        # Initialize ScheduledMonitorThread and InternalMsgQ
        super(SNMPtraps, self).initialize(conf_reader)

        # Initialize internal message queues for this module
        super(SNMPtraps, self).initialize_msgQ(msgQlist)

        self._set_debug(True)
        self._set_debug_persist(True)

        self._get_config()

        return True

    def read_data(self):
        """Return the most recent trap information"""
        return self._latest_trap

    def run(self):
        """Run the sensor on its own thread"""

        # Check for debug mode being activated/deactivated
        self._read_my_msgQ_noWait()

        try:
            #self._log_debug("Start processing")
            logger.debug("Start processing")
            logger.info("Start processing")
            # Create MIB loader to lookup oids sent in traps
            self._mib_builder()

            # to socket transport dispatcher
            snmpEngine = engine.SnmpEngine(v2c.OctetString(
                                hexValue='80001f8880ec70e17424be1f5f00000000'))

            # Transport setup
            # UDP over IPv4
            config.addTransport(
                snmpEngine,
                udp.domainName,
                udp.UdpTransport().openServerMode((
                                self._bind_ip, self._bind_port))
            )
            # UDP over IPv6
            config.addTransport(
                snmpEngine,
                udp6.domainName,
                udp6.Udp6SocketTransport().openServerMode((
                                '::1', self._bind_port))
            )

            # SNMPv3/USM setup
            # this USM entry is used for TRAP receiving purpose
            config.addV3User(snmpEngine, 'inform_sender',
                config.usmHMACSHAAuthProtocol, 'authpass',
                config.usmAesCfb128Protocol, 'privpass',
            )

            # Create an asynchronous dispatcher and register a callback method
            # to handle incoming traps
            # Register SNMP Application at the SNMP engine
            ntfrcv.NotificationReceiver(snmpEngine, self._trap_catcher)

            snmpEngine.transportDispatcher.jobStarted(1)  # this job would never finish

            # Run I/O dispatcher which would receive queries and send
            # confirmations
            try:
                # Dispatcher will never finish as job #1 never reaches zero
                snmpEngine.transportDispatcher.runDispatcher()
            except Exception as ae:
                #self._log_debug("Exception: %r" % ae)
                logger.debug("Exception: %r" % ae)
                logger.info("Exception : %r" % ae)

                snmpEngine.transportDispatcher.closeDispatcher()

            #self._log_debug("Finished processing, restarting SNMP listener")
            logger.debug("Finished processing, restarting SNMP listener")
            logger.info("Finished processing, restarting SNMP listener")

            # Reset debug mode if persistence is not enabled
            self._disable_debug_if_persist_false()

            # Schedule the next time to run thread
            self._scheduler.enter(10, self._priority, self.run, ())

        # Could not bind to IP:port, log it and exit out module
        except Exception as ae:
            logger.info("Unable to process SNMP traps from this node," + \
                        "closing module.")
            logger.info("SNMP Traps sensor attempted to bind to %s:%s" %
                         (self._bind_ip, self._bind_port))

    def _mib_builder(self):
        """Loads the MIB files and creates dicts with hierarchical structure"""

        # Create MIB loader/builder
        mibBuilder = builder.MibBuilder()

        self._log_debug('Reading MIB sources...')
        logger.info('Reading MIB sources...')
        compiler.addMibCompiler(
                        mibBuilder,
                        sources=['/etc/sspl-ll/templates/snmp'])
        # mibSources = mibBuilder.getMibSources() + (
        #     builder.DirMibSource('/etc/sspl-ll/templates/snmp'),)
        # mibBuilder.setMibSources(*mibSources)

        self._log_debug("MIB sources: %s" % str(mibBuilder.getMibSources()))
        logger.info("MIB sources: %s" % str(mibBuilder.getMibSources()))
        # for module in self._enabled_MIBS:
        #     mibBuilder.loadModules(module)
        mibBuilder.loadModules(self._enabled_MIBS)
        self._mibView = view.MibViewController(mibBuilder)

    def _mib_oid_value(self, oid, val):
        """Look up the trap name using the OID in the MIB"""
        ret_val = "N/A"
        nodeDesc = "N/A"
        try:
            # Retrieve information in MIB using the OID
            modName, nodeDesc, suffix = self._mibView.getNodeLocation(oid)
            ret_val = val
            self._log_debug(f'module: {modName}, {nodeDesc}: <{type(val).__name__}> {val.prettyPrint()}, oid: {oid.prettyPrint()}')
            logger.info('module: %s, %s: <%s> %s, oid: %s' % (
                            modName, nodeDesc, type(val).__name__),
                            val.prettyPrint(), oid.prettyPrint()
                        )
            # Lookup the trap name from the SNMP Modules MIB
            if(type(val).__name__ == 'ObjectIdentifier'):
                # Convert the dot notated str oid to a tuple of ints for getNodeName API call
                trap_oid = str(val)
                tmp_oid = trap_oid.split(".")
                tuple_oid = tuple([int(x) for x in tmp_oid])

                oid, label, suffix = self._mibView.getNodeName(tuple_oid)
                self._trap_name = str(label[-1]) + '.'.join(tuple([str(x) for x in suffix]))
                self._log_debug(f'Trap Notification: {self._trap_name}')
                logger.info(f'Trap Notification: {self._trap_name}')
        except Exception as ae:
            self._log_debug("_mib_oid_value: %r" % ae)
            logger.info("_mib_oid_value: %r" % ae)
        return (nodeDesc, ret_val)

    def _trap_catcher(self,snmpEngine, stateReference, contextEngineId,
                      contextName, varBinds, cbCtx):
        """Callback method when a SNMP trap arrives"""
        json_data = {}
        self._trap_name = ""

        logger.info('Notification from ContextEngineId "%s", ContextName "%s"' %
                    (contextEngineId.prettyPrint(), contextName.prettyPrint()))
        for oid, val in varBinds:
            nodeDesc, ret_val = self._mib_oid_value(oid, val)

            # Build up JSON data to be logged in IEM and sent to Halon
            if nodeDesc != "N/A" and ret_val != "N/A":
                json_data[nodeDesc] = ret_val

        self._log_debug(f"trap_name: {self._trap_name}")
        self._log_debug(f"enabled_traps: {self._enabled_traps}")
        logger.info(f"trap_name: {self._trap_name}")
        logger.info(f"enabled_traps: {self._enabled_traps}")

        # Apply filter unless there is an asterisk in the list
        if '*' in self._enabled_traps or self._trap_name in self._enabled_traps:
            # Log IEM
            self._log_iem(json_data)

            # Transmit to Halon
            self._transmit_json_msg(json_data)

    def _log_iem(self, json_data):
        """Create IEM and send to logging msg handler"""
        log_msg = f"IEC: 020004001: SNMP Trap Received, {self._trap_name}"
        internal_json_msg = json.dumps(
                    {"actuator_request_type" : {
                        "logging": {
                            "log_level": "LOG_WARNING",
                            "log_type": "IEM",
                            "log_msg": f"{log_msg}:{json.dumps(json_data, sort_keys=True)}"
                            }
                        }
                     })

        # Send the event to logging msg handler to send IEM message to journald
        self._write_internal_msgQ(LoggingMsgHandler.name(), internal_json_msg)

    def _transmit_json_msg(self, json_data):
        """Transmit message to halon by passing it to egress msg handler"""
        json_data["trapName"] = self._trap_name
        json_msg = SNMPtrapMsg(json_data).getJson()
        self._write_internal_msgQ(RabbitMQegressProcessor.name(), json_msg)

    def _get_config(self):
        """Retrieves the information in /etc/sspl.conf"""
        self._enabled_traps = ['*']
        self._enabled_MIBS = ['AGENTX-MIB.txt',  'IF-MIB.txt', 'NET-SNMP-EXAMPLES-MIB.txt',  'SCTP-MIB.txt', 'SNMPv2-TC.txt',
            'BRIDGE-MIB.txt', 'INET-ADDRESS-MIB.txt', 'NET-SNMP-EXTEND-MIB.txt', 'SMUX-MIB.txt', 'SNMPv2-TM.txt',
            'DISMAN-EVENT-MIB.txt', 'IP-FORWARD-MIB.txt', 'NET-SNMP-MIB.txt', 'SNMP-COMMUNITY-MIB.txt', 'SNMP-VIEW-BASED-ACM-MIB.txt',
            'DISMAN-SCHEDULE-MIB.txt', 'IP-MIB.txt', 'NET-SNMP-PASS-MIB.txt', 'SNMP-FRAMEWORK-MIB.txt', 'TCP-MIB.txt',
            'DISMAN-SCRIPT-MIB.txt', 'IPV6-FLOW-LABEL-MIB.txt', 'NET-SNMP-TC.txt', 'SNMP-MPD-MIB.txt', 'TRANSPORT-ADDRESS-MIB.txt',
            'EtherLike-MIB.txt', 'IPV6-ICMP-MIB.txt', 'NET-SNMP-VACM-MIB.txt', 'SNMP-NOTIFICATION-MIB.txt', 'TUNNEL-MIB.txt',
            'HCNUM-TC.txt', 'IPV6-MIB.txt', 'NETWORK-SERVICES-MIB.txt',   'SNMP-PROXY-MIB.txt', 'UCD-DEMO-MIB.txt',
            'HOST-RESOURCES-MIB.txt', 'IPV6-TCP-MIB.txt','NOTIFICATION-LOG-MIB.txt',   'SNMP-TARGET-MIB.txt', 'UCD-DISKIO-MIB.txt',
            'HOST-RESOURCES-TYPES.txt', 'IPV6-TC.txt', 'SNMP-USER-BASED-SM-MIB.txt',   'UCD-DLMOD-MIB.txt',
            'IANA-ADDRESS-FAMILY-NUMBERS-MIB.txt',  'IPV6-UDP-MIB.txt', 'SNMP-USM-AES-MIB.txt', 'UCD-IPFWACC-MIB.txt',
            'IANAifType-MIB.txt', 'LM-SENSORS-MIB.txt', 'RFC1155-SMI.txt', 'SNMP-USM-DH-OBJECTS-MIB.txt', 'UCD-SNMP-MIB.txt',
            'IANA-LANGUAGE-MIB.txt', 'RFC1213-MIB.txt', 'SNMPv2-CONF.txt', 'UDP-MIB.txt',
            'IANA-RTPROTO-MIB.txt', 'MTA-MIB.txt', 'RFC-1215.txt', 'SNMPv2-MIB.txt',
            'IF-INVERTED-STACK-MIB.txt', 'NET-SNMP-AGENT-MIB.txt', 'RMON-MIB.txt', 'SNMPv2-SMI.txt']
        self._bind_ip = '10.230.240.148'
        self._bind_port = 162
        # self._enabled_traps = self._conf_reader._get_value_list(self.SNMPTRAPS,
        #                                                 self.ENABLED_TRAPS)
        # self._enabled_MIBS  = self._conf_reader._get_value_list(self.SNMPTRAPS,
        #                                                 self.ENABLED_MIBS)

        # self._bind_ip = self._conf_reader._get_value_with_default(self.SNMPTRAPS,
        #                                                 self.BIND_IP,
        #                                                 'service')
        # self._bind_port = int(self._conf_reader._get_value_with_default(self.SNMPTRAPS,
        #                                                 self.BIND_PORT,
        #                                                 1620))

        logger.info("          Listening on %s:%s" % (self._bind_ip, self._bind_port))
        logger.info("          Enabled traps: %s" % str(self._enabled_traps))
        logger.info("          Enabled MIBS: %s" % str(self._enabled_MIBS))

    def shutdown(self):
        """Clean up scheduler queue and gracefully shutdown thread"""
        super(SNMPtraps, self).shutdown()
