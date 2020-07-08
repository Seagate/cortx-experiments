# This test is used to create 0.1 Million objects of 1KB size.
# 1KB content is taken from a preexisting file named [my1kFile.txt] in this case.
# one can use anyfile instead, this modification is required.

from __future__ import print_function
import consul
import os
import subprocess
import time

#c = consul.Consul(host='10.2302.241.123', )
#c = consul.Consul(host='10.230.241.123', port='1301')
#c = consul.Consul()

start = 0
end = 0

def createObjs():
    start = time.time()
    for i in range(100000):
	# To print time interval after 1K entry.
        if i%1000 == 0:
            end = time.time()
            command = 'echo '+'Runtime after '+str((i+1))+' is :'+str((end-start))+'>> logfileInterval.txt' 
            os.system(command)

        filename = 'keyFile_'+str(i)+'.txt'
        
        os.system('consul kv put '+filename+' @my1kFile.txt')

    end = time.time()
    print("Runtime of the program is : ",(end - start))
   

def main():
	createObjs()

if __name__ == '__main__':
    main()

