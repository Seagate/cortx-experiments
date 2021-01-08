#!/bin/bash

a=37

mkdir -p /root/status/
echo "start $(date)" >> /root/status/standby
echo "" >> /root/status/standby

while [ $a -gt 3 ]; do
    n1=`expr $a - 1`
    n2=`expr $a - 2`
    n3=`expr $a - 3`
    echo "start standby $(date) $n1 $n2 $n3" >> /root/status/standby
    pcs cluster standby srvnode-$n1 srvnode-$n2 srvnode-$n3
    a=$(echo $n3)
    while true; do
        nodes=$(pcs status nodes | grep "Standby:")
        echo $nodes | grep srvnode-$n1 && echo $nodes | grep srvnode-$n2 && echo $nodes | grep srvnode-$n3 && break
        echo $nodes
        sleep 5
    done
        echo "done standby $(date) $n1 $n2 $n3" >> /root/status/standby
done

echo "" >> /root/status/standby
echo "end" >> /root/status/standby
