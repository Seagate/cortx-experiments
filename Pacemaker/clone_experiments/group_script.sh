#!/bin/bash

cib_file=cib_cortx_cluster.xml

pcs cluster cib $cib_file

pcs -f $cib_file resource create motr-confd ocf:heartbeat:Dummy --group io-stack
pcs -f $cib_file resource create motr-ios-1 ocf:seagate:clone-service service=motr --group motr_ios
pcs -f $cib_file resource create motr-ios-2 ocf:seagate:clone-service service=motr --group motr_ios
pcs -f $cib_file resource create hax ocf:heartbeat:Dummy --group io-stack
pcs -f $cib_file resource create haproxy  ocf:heartbeat:Dummy --group io-stack
pcs -f $cib_file resource create s3auth  ocf:heartbeat:Dummy --group io-stack
pcs -f $cib_file resource create s3server-1 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-2 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-3 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-4 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-5 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-6 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-7 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-8 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-9 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-10 ocf:seagate:clone-service service=s3server --group s3server
pcs -f $cib_file resource create s3server-11 ocf:seagate:clone-service service=s3server --group s3server

pcs -f $cib_file resource clone motr_ios
pcs -f $cib_file resource clone s3server
pcs -f $cib_file resource clone io-stack

pcs cluster cib-push $cib_file
