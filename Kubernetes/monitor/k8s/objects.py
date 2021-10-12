from monitor.k8s.error import NotSupportedObjectError


class ObjectMap:
    _function_map = {
        'node': 'list_node',
        'pod': 'list_pod_for_all_namespaces'
    }

    @staticmethod
    def get_subscriber_func(object):
        if object in ObjectMap._function_map:
            return ObjectMap._function_map[object]

        raise NotSupportedObjectError(f"object = {object}")

    @staticmethod
    def get_all_objects():
        return ObjectMap._function_map.keys()
