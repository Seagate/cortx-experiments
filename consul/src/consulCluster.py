# This script is used as a consul client to query consul server.
# Make sure you are running this script on a consul server which is already connected to a cluster.
# Purpose of this script is to make sure that your data stays 

from __future__ import print_function
import consul
import os
import subprocess
import socket

# creates a consul client object for the local host
c = consul.Consul()

# To get the list of existing members in the cluster
def ConsulMembers():
    print ("member list  : ")
    mem = c.agent.members(wan=False)
    for var in mem:
        print(var,'\n')

# To perform KV 'put' operation
def KvstorePut():
    key1 = raw_input("enter key : ")
    val1 = raw_input("enter value : ")
    c.kv.put(key1, val1)


# To perform KV 'get' operation
def KvstoreGet():
    key1 = raw_input("Enter key : ")
    T = c.kv.get(key1, index=None)
    print (T[1:])

# To 'get' all the stored keys on consul servers
def KvGetAll():
    cmd = 'consul kv get -recurse'
    os.system(cmd)

	
# To 'delete' all the stored keys on consul servers
def KvDeletekey():
    key = raw_input('Input key to delete')
    c.kv.delete(key)

	
# To query leader info for the cluster
def LeaderInfo():
    print(c.status.leader())
    #print(c.status.peers())

	
# To leave the consul
def LeaveConsul():
    os.system('consul leave')


# To start a session
def startSession():
    print ("starting the session : \n",c.session.create())


# To list all the started sessions
def ListSessions():
    t = c.session.list()
    for i in t[1:]:
        for x in i:
            print (x,'\n')

	
# To perform KV 'put' with a session locking
def KvPutWithLockAcquire():
    session_id = raw_input('provide session_id to acquire lock :\n')
    key = raw_input('provide key :\n')
    val = raw_input('provide value :\n')

    if True == c.kv.put(key, val, acquire=session_id):
        print('Acquisition succeed!\n')
    else:
        print('Acquisition Failed!\n')

	
# To release session lock on a particular key 
def KvPutReleaseLock():
    session_id = raw_input('provide session_id to acquire lock :\n')
    key = raw_input('provide key :\n')
    if True == c.kv.put(key, None, release=session_id):
        print('Release succeed!\n')
    else:
        print('Release Failed!\n')

	
# To destroy created session
def DestroySession():
    session_id = raw_input('Input session_id to destroy!')
    if True == c.session.destroy(session_id):
        print('Destroy succeed!\n')
    else:
        print('Destroy Failed!\n')

	
# To create ACL with your desired rules
# Client options is to be selected for for simple policy creation and application
# Management option allows more flexibility of creating and deleting tokens.
# Make sure you have bootstrap token to pass here as a 'management token'
# Bootstrap token creation can be done using cli command 'consul acl bootstrap' if not created
# Refer to : https://learn.hashicorp.com/consul/security-networking/production-acls#consul-kv-tokens
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

	
# Apply token globally to the agent [To be used only after creating a session]
def ApplyACL():
    acl_id = raw_input("enter ACL token to update global policy :\n")
    os.system('export CONSUL_HTTP_TOKEN=' + acl_id)
    print("ACL applied globally\n")


# To update ACL token with new rules
# Client options is to be selected for for simple policy creation and application
# Management option allows more flexibility of creating and deleting tokens.
# Make sure you have bootstrap token to pass here as a 'management token'
# Bootstrap token creation can be done using cli command 'consul acl bootstrap' if not created
# Refer to : https://learn.hashicorp.com/consul/security-networking/production-acls#consul-kv-tokens
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
        1: ConsulMembers,
        2: KvstorePut,
        3: KvstoreGet,
        4: KvGetAll,
        5: KvDeletekey,
        6: LeaderInfo,
        7: LeaveConsul,
        8: startSession,
        9: ListSessions,
        10: KvPutWithLockAcquire,
        11: KvPutReleaseLock,
        12: DestroySession,
	13: CreateACL,
	14: ApplyACL,
	14: UpdateACL,
    }
    #function call
    switcher[argument]()


def printList():
    print("******************************************\n")
    print("press 1 to see memberlist")
    print("press 2 to put key-val")
    print("press 3 to get val")
    print("press 4 to get all key-val")
    print("press 5 to delete a key-val pari")
    print("press 6 for leader info")
    print("press 7 to leave consul")
    print("press 8 to create a session")
    print("press 9 to list sessions")
    print("press 10 to acquire lock")
    print("press 11 to release lock")
    print("press 12 to destroy session")
    print("press 13 to create ACL")
    print("press 14 to apply ACL globally")
    print("press 15 to update ACL")
    print("******************************************\n")

    choice = int(input())
    Switch(choice)


def main():
    while True:
        printList()


if __name__ == '__main__':
    main()
