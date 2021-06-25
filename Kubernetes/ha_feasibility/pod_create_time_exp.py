import subprocess
import datetime
import json

op = subprocess.Popen('kubectl get pod | awk \'{print $1}\'', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
replica_list = op.communicate()
rs = replica_list[0].decode('ascii').split('\n')
replica_set_1 = set(rs)

count = 1
delete_time = datetime.datetime.now()
pod_delete_time = delete_time.strftime('%H %M %S')
print(f'delete time: {pod_delete_time}')
print('+++++++++++++++++++++++++++++')
l = pod_delete_time.split(' ')

for rs in replica_set_1:
    if rs and count <= 20:
        print(f'delete: {rs} {count}')
        op = subprocess.Popen(f'kubectl delete pod {rs}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        op.communicate()
        count += 1

op = subprocess.Popen('kubectl get pod | awk \'{print $1}\'', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
replica_list = op.communicate()
rs = replica_list[0].decode('ascii').split('\n')
replica_set_2 = set(rs)

intersect_set = replica_set_2 - replica_set_1
print(f'After: {intersect_set}')
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')


for rs in intersect_set:
    if rs:
        op = subprocess.Popen(f'kubectl get pod {rs} -o json', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pod_info = op.communicate()
        str_pod_info = pod_info[0].decode('ascii')
        dict_pod_info = json.loads(pod_info[0].decode('ascii'))

        pod_status_info = dict_pod_info['status']['conditions']

        create_time = pod_status_info[0]['lastTransitionTime']
        container_ready_time = pod_status_info[2]['lastTransitionTime']
        container_fully_ready_time = pod_status_info[1]['lastTransitionTime']

        print(f'container {rs} stats:')
        print(f'Initialize time: {create_time}')
        print(f'containerReady state time: {container_ready_time}')
        print(f'container ready time: {container_fully_ready_time}')

        print('========================================================')


        initialize_datetime_obj = datetime.datetime.strptime(create_time, "%Y-%m-%dT%H:%M:%SZ")
        ready_datetime_obj = datetime.datetime.strptime(container_fully_ready_time, "%Y-%m-%dT%H:%M:%SZ")

        timedifference = ready_datetime_obj - initialize_datetime_obj
        print(f'container: {rs} startup_time(H:M:S): {timedifference}')

