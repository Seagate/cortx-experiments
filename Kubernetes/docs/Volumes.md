## Kubernetes Volumes

- The idea for Kubernetes volumes can basically be thought as a solution for ephemeral on-disk files in a container. On a container crash, the kubelet restarts it but with loss of files and with a clear state. Kubernetes volume helps us to achieve statefulness and also sharing of data between those containers. 

- A Volume is a separate object defined within context of the Kubernetes pod. The volume is associated with the pod but then mounted into a container at a particular path. In Kubernetes there’s a wide variety of different volume implementations, simplest being a temporary volume associated to the pod; called emptyDir. 

Kubernetes volumes have an explicit lifetime; same as of pod that it is associated with. Volume outlives even after container crash and data is preserved. Lifetime of Volume=Lifetime of Pod 

- Some of the volumes supported by Kubernetes: 

  1. awsElasticBlockStore 

  2. Hostpath 

  3. iscsi 

  4. NFS 

  5. emptyDir 

  6. persistentVolumeClaim 

  7. portworxVolume 

  8. azureDisk 

  9. local 
  

Now, though Kubernetes volumes help us solve some problems faced before; but it has one major hitch. If pod ceases to exist, so does the volume. So, we need an upgrade. Here’s where persistent volumes come into picture. 

## Persistent Volumes 

- A Persistent Volume (PV) is a volume plugin (storage) or a resource in Kubernetes cluster provisioned by Kubernetes admin or can be provisioned dynamically using Storage Classes. A PV is a cluster wide resource that can be used to store data in a way that it persists beyond the lifetime of the pod. The PV isn’t backed by locally-attached storage on a worker node but by networked storage system like EBS or NFS. 

- PV’s lifecycle is independent of any individual pod that uses it. For getting a PV user requires Persistent volume Claim (PVC). PVCs consume PV resources. For a pod requesting PV. Basically, it seems like as following for a third person: 

[POD (requests a PV) -> PVC (accepts the request and looks up for a PV with given specs) ->If PV is present it gets bound to the Pod back through PVC] 

But NO. From a pod’s point of view, it thinks PVC is the volume; but in real it’s just a claim. 

- The interaction between PV and PVC has a lifecycle: 

  1. Provisioning
  2. Binding 
  3. Using 
  4. Reclaiming 

- PVs can be provisioned statically and dynamically. 

  - Static: Kubernetes cluster admin creates a number of PVs having details of real storage and are available to cluster users. 

  - Dynamic: The cluster dynamically provisions a volume when none of the static PVs match user’s PVC. The provisioning is based on Storage Class. PVC must request a Storage class and admin must have created and configured that class for dynamic provisioning to occur. In order to enable DP, the admin needs to enable DefaultStorageClass admission controller on API server. 

A control loop in master watches for new PVCs and if matching PV is found, binds it to the pod requesting it. A PVC to PV is a one-to-one mapping. (Using Claimref: A bidirectional binding between PV and PVC). 

No binding is done if matching volume doesn’t exist. Pods use claims as volumes. Once claim finds the volume, the cluster mounts the volume for a Pod. User can specify the mode when using their claim as a volume in a Pod. (if multiple access modes) 

In case if user deletes a PVC, or admin deletes a PV which is in use by a pod, what happens? We might result in data loss? 

NO. Even if we delete the active PVC or admin deletes the PV which is bound to a pod, the deletion doesn’t take place immediately. It is postponed until the PVC or PV is no longer in use by the pod. Thus, saving the data. This is achieved using Storage Object in Use Protection. 

Once a user is done with the PV, deleting of PVC objects from API that allows reclamation of the resource. Volumes can be Retained or Deleted using reclaim policies of same name. 

Recycle policy is not in use for now. 

  

- A Persistent Volume contains specification and status of the Volume. 

For example: SamplePV.yml 

The above mentioned specs are written in a configuration file with .yaml or .yml extension. 

  
```
apiVersion: v1            #(version number) 

kind: PersistentVolume 

metadata: 

    name: PV01          #(any name of PV) 

spec: 

    capacity: 

       storage: 10Gi     #(the volume capacity in gibibytes) 

    volumeMode:       #(Filesystem or Block) 

    accessModes: 

       -( eg: ReadWriteOnce) 

Hostpath:                   #(type of PV eg: nfs, hostpath) 

    Path: “/mnt/sample”    #(the path onto which the volume is to be mount) 

  ```

Note: Everything written in #() is just for understanding purpose. 

  

/mnt/sample says that volume is present at that location on Kubernetes cluster’s node. 

- Creation of Persitent Volume PV can be done using 
```
kubbectl apply -f SamplePV.yml 
```
  

- Verification of created PV using 
```
kubectl get pv PV01 
```
Output: Persitent Volume is Available. (Available doesn’t mean bound) 

  

Similarly, we’ll need to create PersitentVolumeClaim using .yaml file 

For example: SamplePVC.yml 
```
apiVerison: v1 

kind: PersistentVolumeClaim 

metadata: 

    name: PVC01 

spec: 

    accessModes: 

        -ReadWriteOnce 

Resources: 

    Requests: 

       Storage: 5Gi 

  ```

  

 - Creation of a Persistent Volume Claim PVC can be done using 
```
Kubectl apply -f SampleClaim.yml 
```
  

- Verification of created PV claim using 
```
Kubectl get pvc PVC01 
```
  

Now as claim for 5Gi is created and we already have created a PV for 10Gi so, we have a PV satisfying the storage criteria of our given PVC. Now if we look out at the PV again, we’ll surely have status of PV as BOUND which was earlier as AVAILABLE. 

Again, type in: [kubectl get pv PV01]. Even the PVC will show status as BOUND. 

  

Last thing is now to create a Pod that will use this PVC as a Volume. Same through .yml configuration file. 

For example: SamplePOD.yml 
```
apiVerison: v1 

kind: Pod 

metadata: 

    name: POD01 

spec: 

    volumes: 

       -name: StoragePV 

        persistentVolumeClaim: 

             claimName: PVC01 

    containers: 

        -name: PVcontainer 

         Image: nginx 

         Ports: 

              -containerPort: 80 

               Name: “http-server” 

          volumeMounts: 

               -mountPath: “/usr/share/nginx/filename” 

                Name: StoragePV 

  
```
- As said before, from pod’s point of view the PVC is the volume as no PV is specified in the file above. 

  

- Creation of Pod is done using: 
```
Kubectl apply -f SamplePOD.yml 
```
  

- Verification of created POD using 
```
Kubectl get pod POD01 
```
  

So, creation of PV and assigning it to a pod through PVC can be done successfully using above commands. 

  

Deletion of all above created can be done using: 
```
Kubectl delete pod POD01 

Kubectl delete pvc PVC01 

Kubectl delete pv PV01 
```
  

Removing of directory created for volume mount and files can be deleted through shell on your node using rm and rmdir command. (Run as superuser ‘sudo’) 

The types of Persistent volume available in your Kubernetes Cluster depends on the environment whether its On-prem or public cloud. 

  

Now we had PV which solved most of our problems of data preservation and state management up to certain level, but there is a problem over here for some PV like hostpath volume; consider a pod is down and now the Kubernetes scheduler will reschedule the pod. Here it can schedule the pod on any node irrespective of where it was first present. If it gets scheduled in the same node, there isn’t any problem, but if the pod gets rescheduled on a new node the pod cannot regain the data which was stored in PV associated with it before. Hence resulting into data loss. So, to overcome this drawback we have Local persistent volumes. 

  

  

## Local persistent volumes

  

HostPath volumes mount a file or directory from the host node’s filesystem into a Pod. 

A Local Persistent Volume also mounts a local disk or partition into a Pod. The LPV pin points the node association with the persistent volume this helps the Kubernetes scheduler in pod rescheduling process if any pod goes down. 

But the difference here is that the Kubernetes scheduler understands which node a Local Persistent Volume is associated with. While using Local Persistent Volumes, the Kubernetes scheduler ensures that a pod using a Local Persistent Volume is always scheduled to the same node. Data is not lost here as rescheduling of pods is done onto the same node hence PV remains attached and state is preserved and data preservation is done using LPV.  The only way to reference an LPV is through a PVC, there are no other methods. 

 
