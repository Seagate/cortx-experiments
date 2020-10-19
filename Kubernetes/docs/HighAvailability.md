## Kubernetes High Availability  

 

- High Availability:  High Availability in Kubernetes is about setting up Kubernetes cluster, along with its components in such a way that there is no single point of failure and making the system highly reliable. Basically, KHA is about getting a fully reliable, fault-tolerant and robust Cluster setup.  

 

- Achieving High Availability in Kubernetes 

Currently we have 3 node setup with 1 Master and 2 Slaves. But if the master goes down, we fail to create services and pods, etc. But, this can be resolved by multiple master nodes setup. Creating a Cluster of 3 Master and 3 Nodes. Here, if one Master fails; we have remaining ones for backup. 

So, why 3? Why not 4 or 5 or 1000. Discussed later in this document

 

- Is creating multiple masters enough? 

So just creating master nodes isn’t sufficient. A master node comprises of following components: 

  1. Control Plane

  2. API Server 

  3. Control Manager 

  4. Scheduler 

Each of the above-mentioned components need to be replicated on all the master nodes so if one of them fails fails others can keep the cluster up. 

In single master setup all the above components along with etcd DB (Discussed later about etcd later at end in this doc) are managed by master itself. So, if it fails, everything stops and the cluster is lost. So multi-master setup gives us High availability with improved network performance and hence protecting the cluster from wide range of failures. 

Each Master node in multiple master setup runs own copy of all above mentioned components. (Useful for load balancing amongst them) 

 

- Is Multiple Master setup and Kubernetes HA the exact? Or does setting up multiple masters guarantee HA? 

According to my study on KHA; Multiple master setup is not complete HA. I'll explain with an example. Consider 3 master node setup and a single nginx instance in front load balancing. Here though we have 3 masters if nginx goes down, That’s a failure point. 
HA is about eliminating that one failure point! 
Kubernetes in itself is very huge and there can be any component that could fail. If any of the component fails, we are sure to experience an outage. So, we’ll need to dig deeper and analyze the key components and try to eliminate the single point of failure. 


- DATA PLANE 

- etcd is Distributed and consistent key value store that helps reliable storage of data which can be accessed by our Kubernetes cluster (Read and write both). For Kubernetes it is the backend for service discovery and stores cluster state and configuration. It is capable of tolerating machine failure, even in leader node. It also performs graceful leader elections. 

(Multiple etcd replicas are also made in respective master nodes) 

- How does achieving HA work with the components 

apiserver: Easy to run multiple replicas as it is completely stateless. They run in Active Active pattern. All of them can take same request. Simply all of them are active at any point of time. We can add a load balancer in front of those apiservers. 

Scheduler: (Read Act Write on data) Run in an Active Passive pattern. Deciding who will be active is done using locking system. One who acquires lock will be active and rest of them are passive until the active one fails. 

Control Manager: Manages replication and scheduler. 


- So, another way is using management clusters where an unmanaged cluster’s control plane manages another cluster’s control plane as pods. 

- Back to the last component and why 3 nodes? 

Etcd is backed by database and as for any write to a DB to succeed in a cluster environment there needs to be a strict majority to elect a leader that can for the writes to succeed.  

Using multiple active leader-elected peers is one way of making the component highly available. 

- So, why 3 nodes or higher than that? 

The algorithm on which etcd functions is distributed consensus algorithm called raft. Raft uses an equation 

 [(N/2)+1] 

It states that for any action to take place we need a strict majority of least 51% of the members. In etcd’s cluster we need 51% of the members who can reach a quorum on the leader. For example, in etcd we need to have atleast 3 so that we can loose 1 and can have another leader. But it’s not fault resilient anymore.  

I'll explain it in simple words when we loose one we still have 2, which gives 66% coverage of cluster if two are down we just have 33% coverage and it leads to go into Read-only mode. 

Now if we had just 1 etcd that isn’t good. 

If two, one is down its 50%, but we need strict 51% so 3 is the minimum required cluster size. 

Now what if four, in four we need a majority of 3 for above 51% but here fault tolerance remains the same as for 3. i.e. 1. 

So we take 5 to bear two machine failures and better resilience. But scaling involves more cost and resources. And as per my study I think odd no sizes are better at providing highly available clusters. 

- Concluding, you can choose any no of size depend on the business needs of the organization. 

 

## Kubernetes high availability setup using Keepalived system daemon

 

- So, to setup a Kubernetes high availability cluster we require 3 Master nodes and 3 Worker nodes. I.e. 6 VM’s. But if you face resource scarcity; we can have the required setup on only 3 VM’s using ‘Taint’ node option. 

- Generally, while initializing the master node, it is by default configured in such a way that no pod can be scheduled on it. So, if we change the configuration a bit. We can have master as well as worker running on the same node. Thus, resulting into 3M and 3W setup using just 3 VM’s. 

Run as superuser on all nodes 

Check node config using, 

Step I 
```
# kubectl describe node <Enter your Node Name here> 

``` 

Step II 
```
#kubectl taint nodes <your node name> node role.kubernetes.io/master:NoSchedule- 
```
Done, you have one master and one worker on same node. 

**Replicate above steps for all the masters (M1, M2, M3). 

- Verify using same kubectl describe node command.  

You’ll have Taints: <none> 

 

- What is keepalived and why we use it here? 

Keepalived is a piece of software which can be used to achieve high availability by assigning two or more nodes a virtual IP and monitoring those nodes, failing over when one goes down. We use keepalived for failover in this HA setup. Keepalived is available within the standard package repositories. 

 

Step III: Installing Keepalived on all nodes 
```
# Sudo yum install –y keepalived 
```
 

Step IV: Version Check 
```
# keepalived --version 
```
 

Step V: Status check 
```
# systemctl status keepalived 
```

Step VI: Start and enable keepalived 
```
# systemctl start keepalived 

# systemctl enable keepalived 
```
 

Step VII: Configuration of keepalived.conf file on master 1 
```
# cat /etc/keepalived/keepalived.conf 

# cat> /etc/keepalived/keepalived.conf 
```
 

Paste this configuration into the keepalived.conf file 

 

- Configuration File for keepalived 
```
global_defs { 

  router_id LVS_DEVEL 

} 

  

vrrp_script check_apiserver { 

  script "/etc/keepalived/check_apiserver.sh" 

  interval 3 

  weight -2 

  fall 10 

  rise 2 

} 

  

vrrp_instance VI_1 { 

    state MASTER 

    interface eth0 

    virtual_router_id 51 

    priority 101 

    authentication { 

        auth_type PASS 

        auth_pass Seagate@1 

    } 

    virtual_ipaddress { 

        10.230.255.168 

    } 

} 

 ```

Step VIII: Perform Step VII on second and third node also. Just edit state MASTER as state BACKUP and priority 101 as priority 100 in keepalived.conf file on these 2 nodes. Stop keepalived on other two nodes. 

Step IX: Create a file named Kubeadm-config.yaml on first node master 1. 
```
# cat kubeadm-config.yaml 

# cat> kubeadm-config.yaml 
```
 

Paste the following configuration in it 

 
```
apiVersion: kubeadm.k8s.io/v1beta1 

kind: ClusterConfiguration 

kubernetesVersion: stable 

apiServer: 

  certSANs: 

  - "10.230.255.168"       <-- this ip address and your vip should be the same 

networking: 

  podSubnet: 172.16.0.0/16 

controlPlaneEndpoint: "10.230.255.168:6443" 
```
 

Here as we see apiversion v1beta1; it is for old kubernetes version we have kubernetes version 1.18.6. So, we need to upgrade the kubeadm-config.yaml file. 

This can be done using the migrate command  

Step X:  
```
# kubeadm config migrate --old-config kubeadm-config.yaml  --new-config new-kubeadm-config.yaml 
```
 

After running above command check the new-kubeadm-config.yaml file 
```
# cat new-kubeadm-config.yaml 
```
 

*Don’t worry about the file names; you can enter any names for .yaml files. But remember them on your own.  

Now moving onto cluster deployment. Simply interconnecting those nodes. 

Step XI: Initializing Kubernetes cluster on first node so that other two nodes can join this node. 
```
# kubeadm init --config=new_ha_cluster.yaml 
```
 

- Note: This is with swap off. If you have swap enabled add the flag “- -ignore-preflight-errors=Swap” to above command at the end 

 

On successful initialization, a message for joining of control planes and worker nodes will be displayed on master 1.  

- It will look as like follows: 
```
You can now join any number of control-plane nodes by copying certificate authorities 

and service account keys on each node and then running the following as root: 

  

  kubeadm join 10.230.255.168:6443 --token f09qpo.zb5jtbnb94hyn6wi \ 

 --discovery-token-ca-cert-hash sha256:1f0b7f323ecbaef780c3c842aecf581cd057db2c1e4024dfad2dc43e56091ae1 \  --control-plane 

  

Then you can join any number of worker nodes by running the following on each as root: 

  

kubeadm join 10.230.255.168:6443 --token f09qpo.zb5jtbnb94hyn6wi \ 

--discovery-token-ca-cert-hash sha256:1f0b7f323ecbaef780c3c842aecf581cd057db2c1e4024dfad2dc43e56091ae1 

 ```

Step XII: You’ll need to copy certificates and kubeadm configurations generated on master 1 onto other nodes. 

First, you will need to set root user password on master 2 and master3 
```
# passwd 
```
On this prompt enter new root password 

 

Step XIII: Run following on Master 1 
```
NODES="<name of your master2> <name of your master3>" 

CERTS=$(find /etc/kubernetes/pki/ -maxdepth 1 -name '*ca.*' -o -name '*sa.*') 

ETCD_CERTS=$(find /etc/kubernetes/pki/etcd/ -maxdepth 1 -name '*ca.*') 

for NODE in $NODES; do 

  ssh $NODE mkdir -p /etc/kubernetes/pki/etcd 

  scp $CERTS $NODE:/etc/kubernetes/pki/ 

  scp $ETCD_CERTS $NODE:/etc/kubernetes/pki/etcd/ 

  scp /etc/kubernetes/admin.conf $NODE:/etc/kubernetes 

done 

 ```

Step XIII: Copy and Run join command generated by master1 on master2 and 3 respectively.  
```
kubeadm join 10.230.255.168:6443 --token f09qpo.zb5jtbnb94hyn6wi \ 

--discovery-token-ca-cert-hash sha256:1f0b7f323ecbaef780c3c842aecf581cd057db2c1e4024dfad2dc43e56091ae1 \ --control-plane 

 ```

Done! You are now ready with a 3Master and 3Worker Kubernetes High Availability Setup using Keepalived Daemon. 

If you want to verify the working of keepalived, (on all nodes) 
```
# systemctl start keepalived    

# ip –br a 

 ```

On eth0 of first master node you’ll have 2 ip addresses amongst which one will be the virtual ip address assigned by you during configuration. And on other nodes on eth0 you’ll have just one ip addrtess of eth0 but no vip. 

Now if we stop keepalived service on master1; you’ll see the vip shifted onto other node maybe Master2 or master3 as per priority assigned. 

This is how failover works in HA setup through keepalived service. 

 

 

 

 
