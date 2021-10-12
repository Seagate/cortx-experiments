from collections import namedtuple


class K8sAlert:
    def __init__(self):
        self._resource_type = None
        self._resource_name = None
        self._event_type = None
        self._k8s_container = None
        self._pod = None
        self._node = None
        self._is_status = False

    @property
    def resource_type(self):
        return self._resource_type

    @resource_type.setter
    def resource_type(self, res_type):
        self._resource_type = f"k8s:{res_type}"

    @property
    def resource_name(self):
        return self._resource_name

    @resource_name.setter
    def resource_name(self, res_name):
        self._resource_name = res_name

    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        self._event_type = event_type

    @property
    def k8s_container(self):
        return self._k8s_container

    @k8s_container.setter
    def k8s_container(self, name):
        self._k8s_container = name

    @property
    def pod(self):
        return self._pod

    @pod.setter
    def pod(self, name):
        self._pod = name

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, name):
        self._node = name

    @property
    def is_status(self):
        return self._is_status

    @is_status.setter
    def is_status(self, status):
        self._is_status = status

    def to_dict(self):
        return vars(self)

    @staticmethod
    def to_alert(obj_dict):
        return namedtuple('K8sAlert', obj_dict.keys())(*obj_dict.values())
