# This is a file contains functions related to ACL functionalities.
# This details will be used by consulCluster.py

from __future__ import print_function
import consul
import os
import subprocess
#import socket
  
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
    
