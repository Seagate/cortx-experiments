
Following tasks were conducted as part of this POC

1. Explore isci fencing in a VM cluster with remote nodes

	- 	configuration : 
		- A VM cluster containing 2 cluster nodes and 1 remote node; scsi STONITH resources configured in the cluster. 
		- scsi target configured on a seperate VM 
		- scsi clients configured on each cluster and remote nodes 
  
                
	-	Reference for scsi configuration:  
		https://github.com/Seagate/cortx-experiments/blob/main/Stonith/docs/scsi/configure_scsi.md
		https://github.com/Seagate/cortx-experiments/blob/master/Stonith/docs/scsi/scsi_stonith.md
		https://www.server-world.info/en/note?os=CentOS_8&p=iscsi&f=1

	-	Reference for pacemaker cluser configuration 
		https://github.com/Seagate/cortx-ha/wiki/Corosync-Pacemaker-Setup


	-	Attempted creating this configuration 

		 - confirmed that the partitions required by scsi get created on all cluser nodes and remote node. 
		 - In this setup it is not possible to create a scsi based STONITH resource.
		 - If such a resource is created, services running on remote node stop and can not be started 
		 - If the remote node is removed from the cluster, scsi based STONITH resource can be created and
           fencing works fine 		 

	-	On research found some references that "Stonith resource only run on full cluster nodes and not on pacemaker remote nodes"
	    example link :  https://lists.rdoproject.org/pipermail/users/2018-October/000350.html 

	Conclusion: 
		scsi STONITH devices are used for self fencing.
		since it is not possible to start STONITH resources on remote nodes, self fencing of remote nodes is not possible


2. Explaore fencing with ipmi in a cluster with remote nodes 

	- 	Full configuration : 
		- A hardware cluster containing 2 cluster nodes and 1 remote node; ipmi STONITH resources configured in the cluster. 

	- Steps: 
		- created a cluster containing 2 cluster nodes 
		- configured ipmi STONITH resources on both the nodes
		- Added a remote node to this cluster.
		- Tried enabling ipmi STONITH resource on the remote node.
		- Resource did not get enabled there confirming the behaviour seen on VM deployment; that is already mentioned in point 1. 


3. Expolore the need of having a STONITH resource running on remote node

		a. Identify scenarios when a remote node might have to be fenced.
				Two situations were identified:
				- If the remote node becomes unresponsive / unreachable, it needs to be fenced
					Solution : 	The remote node exists as a resource in the system. 
								This resource can be stopped.
								This will trigger fencing for the remote node
				- If a resource running on remote node becomes unresponsive 	
					Solution:	In this situation, the remote node should be fenced and 
								the resources running on it should be moved to another node. 
								
				In both these situations self fencing is not necessary. As long as a cluster node can fence the 
				remote node we should be fine. 	
	
		
		Following experiments were conducted to confirm the abovementioned cases :
		
		b. Check if STONITH of remote node can be triggered from cluster node
				- Configured a cluster with 2 cluster nodes and 1 remote node. 
				- Configured activepassive resources and cloned resources in this cluster.
				- Added ipmi STONITH resources to this cluster. 
				- Tried cloning the STONITH resources and confirmed that STONITH resources do not get started on the remote node in hardware cluster also.
				- Made the remote node unreachble by making its ip link as DOWN 
				  observed in this case that the remote node is fenced and 
				  the active resource running on remote node moves to another cluster node.			
                				
		b. Check if a resource running on remote node becomes unresponsives, does the remote device get fenced
				- Configured a cluster with 2 cluster nodes and 1 remote node. 
				- Configured activepassive resources and cloned resources in this cluster.
				- Added ipmi STONITH resources to this cluster. 
				- Created a resource on the remote node with small value of its stop timeout (pcs resource update s3 op stop timeout=2s) and 
				  increased the stop time (ExecStop) taken by this resource in its service file. (ExecStop=/usr/bin/sleep 120; pkill -f s3backgroundproducer)
				  This ensured that the resource will not stop before its timeout is hit 
				- Tried disabling this resource.  
				- Saw that
					The resource is reported as FAILED.
					The remore node and services running on it are marked as UNCLEAN in cluster status
					Fencing action for the remote node is triggered
					Remaining resources running on the remote node are moved to another node by the fencing action	
				 
				
		c. Check what happens if remote node becomes unresponsive but STONITH resources are not configured in the cluster 
				- Configured a cluster with 2 cluster nodes and 1 remote node. 	
				- Configured activepassive resources and cloned resources in this cluster.
				- Made the remote node unreachble by making its ip link as DOWN
				- Saw that 
					Resources running on remote are marked as UNCLEAN
					Remote node is marked as UNCLEAN
					The remote resource is marked as FAILED
					No resource movement happens


Conclusion : Running a STONITH resouce on remote node is not possible ; 
			 however when required, the remote node can be fenced by a cluster node

Further details regarding the experiments are avilabe in the comments section of EOS-16832