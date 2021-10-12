from monitor.k8s.object_monitor import ObjectMonitor

if __name__ == "__main__":
    object_threads = []
    # Read I/O pod selector label from ha.conf
    pod_label = 'dummy'

    kwargs = {'pretty': True}
    # Change to multiprocessing
    node_thread = ObjectMonitor('node', **kwargs)
    kwargs['label_selector'] = f'app={pod_label}'
    pod_thread = ObjectMonitor('pod', **kwargs)

    pod_thread.start()
    node_thread.start()

    object_threads.append(pod_thread)
    object_threads.append(node_thread)

    for a_thread in object_threads:
        a_thread.join()

    print("All threads have exited.")
