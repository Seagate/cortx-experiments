class K8SEventsConst:
    TYPE = 'type'
    RAW_OBJECT = 'raw_object'
    METADATA = 'metadata'
    NAME = 'name'
    SPEC = 'spec'
    NODE_NAME = 'nodeName'
    PHASE = 'phase'
    RUNNING = 'Running'
    STATUS = 'status'
    CONDITIONS = 'conditions'
    READY = 'Ready'
    true = 'true'


class EventStates:
    ADDED = 'ADDED'
    MODIFIED = 'MODIFIED'
    DELETED = 'DELETED'


class AlertStates:
    ONLINE = 'online'
    OFFLINE = 'offline'
    FAILED = 'failed'
