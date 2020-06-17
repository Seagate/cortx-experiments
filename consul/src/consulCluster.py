from __future__ import print_function
import consul
import os
import subprocess
import socket

c = consul.Consul( )
#c = consul.Consul(host='10.230.241.123', port='1301')
#c = consul.Consul(host='10.230.243.145',port=8301, scheme='http', verify=False)

def startAgent():
    #os.system("start ls /k dir")
    #subprocess.call('ls', shell=True)
    agentType = ''
    if int(raw_input(' Press 0: client mode\n Press 1: server mode\n')):
        agentType = 'server'
    nodeName = raw_input('enter node name you want to create!\n')
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("Try running agent", ip_address, " in ",agentType," mode by running following command in other terminal :\n")
    cmd = 'sudo consul agent -'+agentType+' -bind='+ip_address+' -node='+nodeName+' -data-dir=/tmp/consul -config-dir=/etc/consul.d\n'
    print(cmd)
    #os.system(cmd)

def JoinCluster():
    #c.agent.join('10.230.241.123', wan=False)
    cmd = 'consul join 10.230.241.123'
    os.system(cmd)


def ConsulMembers():
    print ("member list  : ")
    mem = c.agent.members(wan=False)
    for var in mem:
        print(var)


def KvstorePut():
    key1 = raw_input("enter key : ")
    val1 = raw_input("enter value : ")
    c.kv.put(key1, val1)


def KvstoreGet():
    key1 = raw_input("Enter key : ")
    T = c.kv.get(key1, index=None)
    print (T[1:])

def KvGetAll():
    cmd = 'consul kv get -recurse'
    os.system(cmd)

def KvDeletekey():
    key = raw_input('Input key to delete')
    cmd = 'cosnul kv delte ',key

def LeaderInfo():
    print(c.status.leader())
    #print(c.status.peers())

def RestartAgent():
    print ("leaving consul")
    os.system('consul leave')

def LeaveConsul():
    os.system('consul leave')

def Switch(argument):
    switcher = {
        1: startAgent,
        2: JoinCluster,
        3: ConsulMembers,
        4: KvstorePut,
        5: KvstoreGet,
        6: KvGetAll,
        7: KvDeletekey,
        8: LeaderInfo,
        9: RestartAgent,
        0: LeaveConsul,
    }
    switcher[argument]()


def printList():
    print("******************************************\n")
    print("press 1 for starting an agent")
    print("press 2 for Joining a member to cluster")
    print("press 3 to see memberlist")
    print("press 4 to put key-val")
    print("press 5 to get val")
    print("press 6 to get all key-val")
    print("press 7 to delete a key-val pari")
    print("press 8 for leader info")
    print("press 9 to restart an agent")
    print("press 0 to leave consul\n")
    print("******************************************\n")

    choice = int(input())
    Switch(choice)


def main():
    while True:
        printList()


if __name__ == '__main__':
    main()




