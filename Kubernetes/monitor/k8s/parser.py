from monitor.k8s.error import NotSupportedObjectError
from monitor.k8s.const import K8SEventsConst
from monitor.k8s.const import AlertStates
from monitor.k8s.const import EventStates
from monitor.k8s.alert import K8sAlert


class ObjectParser:
    def __init__(self):
        pass

    def parse(self, an_event, cached_state):
        pass


class NodeEventParser(ObjectParser):
    def __init__(self):
        super().__init__()
        self._type = 'node'

    def parse(self, an_event, cached_state):
        alert = K8sAlert()
        alert.resource_type = self._type

        if K8SEventsConst.TYPE in an_event:
            alert.event_type = an_event[K8SEventsConst.TYPE]
        if K8SEventsConst.NAME in an_event[K8SEventsConst.RAW_OBJECT][K8SEventsConst.METADATA]:
            alert.resource_name = an_event[K8SEventsConst.RAW_OBJECT][K8SEventsConst.METADATA][K8SEventsConst.NAME]

        ready_status = None
        try:
            for a_condition in an_event[K8SEventsConst.RAW_OBJECT][K8SEventsConst.STATUS][K8SEventsConst.CONDITIONS]:
                if a_condition[K8SEventsConst.TYPE] == K8SEventsConst.READY:
                    ready_status = a_condition[K8SEventsConst.STATUS]
        except Exception as e:
            pass

        if ready_status is None:
            # Log
            cached_state[alert.resource_name] = ready_status
            return None

        if alert.event_type == EventStates.ADDED:
            cached_state[alert.resource_name] = ready_status.lower()
            if ready_status.lower() == K8SEventsConst.true:
                alert.event_type = AlertStates.ONLINE
                return alert
            else:
                return None

        if alert.event_type == EventStates.MODIFIED:
            if alert.resource_name in cached_state:
                if cached_state[alert.resource_name] != K8SEventsConst.true and ready_status.lower() == K8SEventsConst.true:
                    cached_state[alert.resource_name] = ready_status.lower()
                    alert.event_type = AlertStates.ONLINE
                    return alert
                elif cached_state[alert.resource_name] == K8SEventsConst.true and ready_status.lower() != K8SEventsConst.true:
                    cached_state[alert.resource_name] = ready_status.lower()
                    alert.event_type = AlertStates.FAILED
                    return alert
                else:
                    # Log
                    return None
            else:
                # Log
                return None

        # Handle DELETED event - Not required for Cortx

        return None


class PodEventParser(ObjectParser):
    def __init__(self):
        super().__init__()
        self._type = 'pod'

    def parse(self, an_event, cached_state):
        alert = K8sAlert()
        alert.resource_type = self._type

        if K8SEventsConst.TYPE in an_event:
            alert.event_type = an_event[K8SEventsConst.TYPE]
        if K8SEventsConst.NAME in an_event[K8SEventsConst.RAW_OBJECT][K8SEventsConst.METADATA]:
            alert.resource_name = an_event[K8SEventsConst.RAW_OBJECT][K8SEventsConst.METADATA][K8SEventsConst.NAME]
        if K8SEventsConst.NODE_NAME in an_event[K8SEventsConst.RAW_OBJECT][K8SEventsConst.SPEC]:
            alert.node = an_event[K8SEventsConst.RAW_OBJECT][K8SEventsConst.SPEC][K8SEventsConst.NODE_NAME]

        ready_status = None
        try:
            for a_condition in an_event[K8SEventsConst.RAW_OBJECT][K8SEventsConst.STATUS][K8SEventsConst.CONDITIONS]:
                if a_condition[K8SEventsConst.TYPE] == K8SEventsConst.READY:
                    ready_status = a_condition[K8SEventsConst.STATUS]
        except Exception as e:
            pass

        if ready_status is None:
            # Log
            cached_state[alert.resource_name] = ready_status
            return None

        if an_event[K8SEventsConst.TYPE] == EventStates.ADDED:
            cached_state[alert.resource_name] = ready_status.lower()
            if ready_status.lower() != K8SEventsConst.true:
                return None
            else:
                alert.event_type = AlertStates.ONLINE
                return alert

        if alert.event_type == EventStates.MODIFIED:
            if alert.resource_name in cached_state:
                if cached_state[alert.resource_name] != K8SEventsConst.true and ready_status.lower() == K8SEventsConst.true:
                    cached_state[alert.resource_name] = ready_status.lower()
                    alert.event_type = AlertStates.ONLINE
                    return alert
                elif cached_state[alert.resource_name] == K8SEventsConst.true and ready_status.lower() != K8SEventsConst.true:
                    cached_state[alert.resource_name] = ready_status.lower()
                    alert.event_type = AlertStates.FAILED
                    return alert
                else:
                    # Log
                    return None
            else:
                # Log
                return None

        # Handle DELETED event - Not required for Cortx

        return None


class EventParser:
    parser_map = {
        'node': NodeEventParser(),
        'pod': PodEventParser()
    }

    @staticmethod
    def parse(k_object, an_event, cached_state):
        if k_object in EventParser.parser_map:
            object_event_parser = EventParser.parser_map[k_object]
            return object_event_parser.parse(an_event, cached_state)

        raise NotSupportedObjectError(f"object = {k_object}")

