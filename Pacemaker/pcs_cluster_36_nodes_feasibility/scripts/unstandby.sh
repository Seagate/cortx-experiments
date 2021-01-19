#!/bin/bash


a=0

mkdir -p /root/status/
echo "start $(date)" >> /root/status/unstandby
echo "" >> /root/status/unstandby

while [ $a -lt 36 ]; do
    n1=`expr $a + 1`
    n2=`expr $a + 2`
    n3=`expr $a + 3`
    echo "start unstandby $(date) $n1 $n2 $n3" >> /root/status/unstandby
    pcs cluster unstandby srvnode-$n1 srvnode-$n2 srvnode-$n3
    a=$(echo $n3)
    while true; do
        nodes=$(pcs status nodes | grep "Online:")
        echo $nodes | grep srvnode-$n1 && echo $nodes | grep srvnode-$n2 && echo $nodes | grep srvnode-$n3 && break
        echo $nodes
        sleep 5
    done
        while true; do
                pcs resource | grep "srvnode-$n1 " | grep Stopped && pcs resource | grep "srvnode-$n2 " | grep Stopped && pcs resource | grep "srvnode-$n3 " | grep Stopped || break
                sleep 10
        done
        echo "done unstandby $(date) $n1 $n2 $n3" >> /root/status/unstandby
done

echo "" >> /root/status/unstandby
echo "end $(date)" >> /root/status/unstandby
