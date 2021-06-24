import subprocess
import datetime
import time

def get_count():
    op = subprocess.Popen('kubectl get pod | grep -c \'Running\'', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    count = op.communicate()
    count = count[0].decode('ascii').split('\n')[0]
    print(count)
    if int(count) >= 100:
        return
    print(f'POD count: {count}')
    print('Wait till the replaced replica for deleted one comes back: 5 sec')
    time.sleep(5)
    get_count()

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
    if rs and count <= 1:
        print(f'delete: {rs} {count}')
        op = subprocess.Popen(f'kubectl delete pod {rs}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        op.communicate()
        count += 1

get_count()

op = subprocess.Popen('kubectl get pod | awk \'{print $1}\'', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
replica_list = op.communicate()
rs = replica_list[0].decode('ascii').split('\n')
replica_set_2 = set(rs)
print(replica_set_2)

intersect_set = replica_set_2 - replica_set_1
print(f'Newly created POD after deletion: {intersect_set}')


for rs in intersect_set:
    if rs:
        op = subprocess.Popen(f'kubectl describe pod {rs}' + ' | grep \'Start Time:\' | awk \'{print $7}\'', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        t = op.communicate()
        create_time = t[0].decode('ascii').strip('\n')
        print(f'create time: {create_time}')
        print('+++++++++++++++++++++++++++++')
        l1 = create_time.split(':')
        if int(l1[0]) > int(l[0]):
            h_diff = int(l1[0]) - int(l[0])
            print(f'hours to get up: {h_diff}')
            print('+++++++++++++++++++++++++++++')
        elif int(l1[1]) > int(l[1]):
            l_dif = int(l1[1]) - int(l[1])
            print(f'minutes to get up: {l_dif}')
            print('+++++++++++++++++++++++++++++')
        elif int(l1[2]) > int(l[2]):
            s_dif = int(l1[2]) - int(l[2])
            print(f'seconds of difference {s_dif}')
            print('+++++++++++++++++++++++++++++')
