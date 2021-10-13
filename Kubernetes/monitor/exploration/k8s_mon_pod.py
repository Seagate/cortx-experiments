from kubernetes import config, client, watch


SEP = '<>'

def compare_dicts(dict1, dict2):
    simple_dict1 = {}
    simple_dict2 = {}
    key = 'head'
    se_dict(dict1, key, simple_dict1)
    for a_key in simple_dict1:
        print(f"{a_key} = {simple_dict1[a_key]}")
    #print(key)
    #print(simple_dict1)
    se_dict(dict2, key, simple_dict2)
    #print(simple_dict2)

    not_found_one = []
    not_found_two = []
    different = {}

    for a_key in simple_dict1:
        if a_key in simple_dict2:
            if simple_dict1[a_key] != simple_dict2[a_key]:
                different[a_key] = [simple_dict1[a_key], simple_dict2[a_key]]
        else:
            not_found_two.append(f"{a_key} = {simple_dict1[a_key]}")

    for a_key in simple_dict2:
        if a_key not in simple_dict1:
            not_found_one.append(f"{a_key} = {simple_dict2[a_key]}")

    print("DIFFERENT........................................")
    for a_key in different:
        print(f"{a_key} : {different[a_key]}")
    print("NOT IN ONE.......................................")
    for an_entry in not_found_one:
        print(an_entry)
    print("NOT IN TWO.......................................")
    for an_entry in not_found_two:
        print(an_entry)


def se_dict(a_dict, key, r_dict):
    if not isinstance(a_dict, dict) and not isinstance(a_dict, list):
        r_dict[key] = a_dict
        return
    if isinstance(a_dict, dict) and len(a_dict.keys()) == 0:
        r_dict[key] = None
        return

    if isinstance(a_dict, list):
        for i, value in enumerate(a_dict):
            se_dict(a_dict[i], key+'_'+str(i), r_dict)

    else:
        for a_key in a_dict:
            se_dict(a_dict[a_key], key+SEP+a_key, r_dict)


config.load_kube_config()
kube_client = client.CoreV1Api()
kube_watch = watch.Watch()
past_modified_events = {}

count = 100
for an_event in kube_watch.stream(kube_client.list_pod_for_all_namespaces, label_selector='app=dummy', pretty=True):
    del an_event['object']
    #print(f"Event = {an_event}")
    compare_dicts(an_event, an_event)
    event_type = name = nodeName = None
    if 'type' in an_event:
        event_type = an_event['type']
    if 'name' in an_event['raw_object']['metadata']:
        name = an_event['raw_object']['metadata']['name']
    if 'nodeName' in an_event['raw_object']['spec']:
        nodeName = an_event['raw_object']['spec']['nodeName'] 
    print(f"Event Type = {event_type}, Pod = {name}, Node = {nodeName}")
    if event_type == 'ADDED':
        past_modified_events[name] = an_event
    if event_type == 'MODIFIED' and name in past_modified_events:
        compare_dicts(past_modified_events[name], an_event)
        past_modified_events[name] = an_event
    if event_type == 'DELETED' and name in past_modified_events:
        compare_dicts(past_modified_events[name], an_event)
        del past_modified_events[name]
    print("****************************************************************************")
    print("****************************************************************************")
    count -= 1
    if count == 0:
        kube_watch.stop()

