#!/bin/bash

#coopyright (c) 2020 Seagate Technoechoy LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>. For any questions
# about this software or licensing, please email opensource@seagate.com or
# cortx-questions@seagate.com.

help() {
    echo """
    Action: add_host, setup, add
    $ config.sh config_ssh ip node_id
    $ config.sh setup init node_id
    $ config.sh setup add node_id
    $ config.sh add_node ip node
    """
}

config_ssh() {
    ip=$2
    node_id=$3
    echo $ip $node_id

    cat /etc/hosts | grep "$node_id " && {
        echo "ip already exists";
    } || echo $ip $node_id  >> /etc/hosts

    cat ~/.ssh/known_hosts | grep "$node_id," || {
        echo "Login to system with ssh and exit then run below command"
        echo "sshpass -p Seagate ssh-copy-id root@$node_id"
        exit;
    }

    awk '{print $NF}' /etc/hosts > /tmp/nodelist
    cat /tmp/nodelist | xargs -I %REPL scp /etc/hosts root@%REPL:/etc/hosts
}

setup() {
    setup=$2
    node=$3
    echo $setup $node

	echo $setup | grep "remote" && {
        #Disable firewall dameon
        ssh root@$node "systemctl stop firewalld"
        ssh root@$node "systemctl disable firewalld"

        #Install corosync, pacemaker
        ssh root@$node "curl https://raw.githubusercontent.com/Seagate/cortx-prvsnr/cortx-1.0/cli/src/cortx-prereqs.sh -o cortx-prereqs.sh; chmod a+x cortx-prereqs.sh; ./cortx-prereqs.sh --disable-sub-mgr"

        ssh root@$node "yum -y install pcs pacemaker-remote resource-agents"
        ssh root@$node "mkdir -p --mode=0750 /etc/pacemaker"
        ssh root@$node "chgrp haclient /etc/pacemaker"
        ssh root@$node "echo Seagate | passwd --stdin hacluster"


        ssh root@$node "systemctl enable pacemaker_remote.service"
        ssh root@$node "systemctl start pacemaker_remote.service"

        scp /etc/pacemaker/authkey root@$node:/etc/pacemaker/authkey
        printf 'hacluster\nSeagate\n' | pcs cluster auth $node
        pcs cluster node add-remote $node

        exit 0
    }

    scp new_node.sh root@$node:/root/new_node.sh
    ssh root@$node "chmod +x /root/new_node.sh"
    ssh root@$node "/root/new_node.sh"

    echo $setup | grep "init" && {
        ssh root@$node "printf 'hacluster\nSeagate\n' | pcs cluster auth $node"
        ssh root@$node "pcs cluster setup --name HA_cluster $node"
        ssh root@$node "pcs cluster start --all"
        ssh root@$node "pcs cluster enable --all"
        ssh root@$node "pcs property set stonith-enabled=false"
        ssh root@$node "pcs property set no-quorum-policy=ignore"
        ssh root@$node "pcs status"
    } || {
        # add node must run from primery node.
        printf "hacluster\nSeagate\n" | pcs cluster auth $node
        pcs cluster node add $node --enable --start
        pcs status | grep "Online" | grep $node || {
            echo "failed to add node"
        }
    }
}

add_node() {
    # add_node ip node
    ip=$2
    node=$3
    config_ssh config $ip $node
    setup setup add $node
}

remote_add() {
    # add remote node
    ip=$2
    node=$3
    config_ssh config $ip $node
    setup setup remote $node
}

remove_node() {
    node=$2
    pcs cluster node remove $node
}

Action=$1

[ -z $Action ] && Action="help"

$Action action $2 $3