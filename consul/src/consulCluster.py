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
        print(var,'\n')


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
    c.kv.delete(key)

def LeaderInfo():
    print(c.status.leader())
    #print(c.status.peers())

def startSession():
    print ("starting the session : \n",c.session.create())

def LeaveConsul():
    os.system('consul leave')

def ListSessions():
    t = c.session.list()
    for i in t[1:]:
        for x in i:
            print (x,'\n')

def KvPutWithLockAcquire():
    session_id = raw_input('provide session_id to acquire lock :\n')
    key = raw_input('provide key :\n')
    val = raw_input('provide value :\n')

    if True == c.kv.put(key, val, acquire=session_id):
        print('Acquisition succeed!\n')
    else:
        print('Acquisition Failed!\n')

def KvPutReleaseLock():
    session_id = raw_input('provide session_id to acquire lock :\n')
    key = raw_input('provide key :\n')
    if True == c.kv.put(key, None, release=session_id):
        print('Release succeed!\n')
    else:
        print('Release Failed!\n')

def DestroySession():
    session_id = raw_input('Input session_id to destroy!')
    if True == c.session.destroy(session_id):
        print('Destroy succeed!\n')
    else:
        print('Destroy Failed!\n')


def CreateACL():
    tInput = int(raw_input('enter 0 for "management" token\nenter 1 for "client" token\n'))
    rule = None
    if tInput == 0:
        tokenType = 'management'
    else:
        tokenType = 'client'
    
    tokenName = raw_input('Name of the token[Optional]\n')
    rule = raw_input('Enter rule for this token [Note: Json or Hcl format is must\n]')
    bootStrapToken = raw_input("enter bootstrap/management token to perfomr token update\n")
    
    #management token passing is must[bootstrap token is something one can use]
    token_id = c.acl.create(name=tokenName, type=tokenType, rules=rule, acl_id=None, token=bootStrapToken)

    print('acl_id is : ', token_id)



def UpdateACL():
    tInput = int(raw_input('enter 0 for "management" token\nenter 1 for "client" token\n'))
    rule = None
    if tInput == 0:
        tokenType = 'management'
    else:
        tokenType = 'client'
    
    acl_id = raw_input("enter token to update policy :\n")
    bootStrapToken = raw_input("enter bootstrap/management token to perform token update\n")
    rule = raw_input('Enter rule for this token [Note: Json or Hcl format is must\n]')
    token_id = c.acl.update(acl_id, name=None, type=tokenType, rules=rule, token=bootStrapToken)
    
    print('ACL update returns : ', token_id)
    

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
        9: startSession,
        0: LeaveConsul,
        11: ListSessions,
        12: KvPutWithLockAcquire,
        13: KvPutReleaseLock,
        14: DestroySession,
	    15: CreateACL,
	    16: UpdateACL,
    }
    #function call
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
    print("press 9 to create a session")
    print("press 0 to leave consul")
    print("press 11 to list sessions")
    print("press 12 to acquire lock")
    print("press 13 to release lock")
    print("press 14 to destroy session")
    print("press 15 to create ACL")
    print("press 16 to update ACL")
    print("******************************************\n")

    choice = int(input())
    Switch(choice)


def main():
    while True:
        printList()


if __name__ == '__main__':
    main()
