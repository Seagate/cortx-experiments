# Scripts

## `config.sh`
- It is to setup and scale cluster.
```
# setup first node in cluster
./config.sh setup init <srvnode-id>
# Add normal node
./config.sh add_node <ip> <srvnode-id>
# Add remote node
./config.sh remote_add <ip> <srvnode-id>
```

## `s3_motr_setup.sh`
- It copy s3server, motr service and configure s3 and motr resource.
- Make sure /etc/hosts and password less ssh set properly.
```
./s3_motr_setup.sh
```

## `add_node_resource.sh`
- Add resources.
- Try to run on minimum node and then scale node.
```
./add_node_resource.sh
```

## `standby.sh`
- Put all node in Standby
- Here in 36 node we can not put all node in standby so we need to put node in some set.
- Here this script put 3 node in standby at a time.
```
./standby.sh
```

## `unstandby.sh`
- Put all node in unstandby.
- It put 3 node in standby at time.
- Consider 1 to 32 are normal and 33 to 36 are remote node.
```
./unstandby.sh
```

##
