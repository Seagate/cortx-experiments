
## CNI

- CNI stands for Container Networking Interface and its goal is to create a generic plugin-based networking solution for containers
- Example
    - Funnale
    - Wave
- Setup
```
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
```
- Ref
    - https://chrislovecnm.com/kubernetes/cni/choosing-a-cni-provider/
    - https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/


## MultContainer Pod Communication
- Pod can contain multiple container where they can communicate to each other using localhost.
- Example: nodejs server is on port 3000 and nginx forword traffic from 3000 to 5000 using localhost

```
$ kubectl create -f multicontainer/nginx_config.yaml
$ kubectl create -f multicontainer/helloworld.yml
$ kubectl describe pod/nodehelloworld.example.com
$ curl <pod-ip>:5000
$ curl <pod-ip>:3000
```

## Pod to node Communication

```
$ kubectl create -f pod_to_node/helloworld.yml
$ kubectl create -f pod_to_node/helloworld-nodeport-service.yml
$ kubectl get svc
```
- Open in browser http://<node-name>:31001/
- Use Case: NodePort is port which same on each node accessible externally and forwarding pod traffic
- If want to access outside of node then add firewall rule for port
- Default NodePort limit: 30000-32767

## Node to Pod

- Use: DNS (CNI) resolve outside node ip and accessible to pod. In pod we need to open container port.

```
$ node node_to_pod/index.js
$ kubectl create -f node_to_pod/nginx_config.yaml
$ kubectl create -f node_to_pod/nginx.yaml
$ kubectl describe pod nginx-pod
$ curl <pod-ip>:5000
```

## Pod to Pod

- Create Pod and then NodePort service for Pod
- Inside pod we can access service using <service-name>:port
- /etc/resolve.conf has entry for namesarver
- Inside pod use $ nslookup <service-name>.default

```
$ kubectl create -f pod_to_pod/helloworld.yaml
$ kubectl create -f pod_to_pod/helloworld_service.yaml
$ kubectl create -f pod_to_pod/nginx_config.yaml
$kubectl create -f pod_to_pod/nginx.yaml
$ kubectl describe pod nginx-pod
$ curl <pod-ip>:5000
```


