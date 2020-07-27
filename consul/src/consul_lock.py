# This is a file contains functions related to Locking using session functionalities.
# This functions will be used by consulCluster.py

from __future__ import print_function
import consul
import os
import subprocess
import socket

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
