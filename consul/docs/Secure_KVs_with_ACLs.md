## Secure KV Using ACLs 

1. All servers are supposed to have a config file acl.json in config directory. 

  `
    
    { 

    "acl": 
      { 

        "enabled": true, 

        "default_policy": "deny", 

        "down_policy": "extend-cache" 

      } 

    }
  
  ` 

2. Restart all the servers one by one [make sure everything starts perfectly fine] 

  `
  
    [INFO] acl: Created the anonymous token 

    [INFO] consul: ACL bootstrap enabled 

    [INFO] agent: Synced node info 

    [WARN] agent: Coordinate update blocked by ACLs 

    [INFO] acl: initializing acls 

    [INFO] consul: Created ACL 'global-management' policy 

  `
    
3. consul acl bootstrap

  * commnad will return
  
    `[root@ssc-vm-0434 rajkumar]# consul acl bootstrap`
    
    `AccessorID:       34052eaf-0db7-9527-eba9-195d6fc4a3f1`
    
    `SecretID:         6bac6b50-8df2-7f1d-aa0a-317ebcdd56fa`
    
    `Description:      Bootstrap Token (Global Management)`
    
    `Local:            false`
    
    `Create Time:      2020-07-09 22:57:20.986767583 -0600 MDT`
    
    `Policies:`
    
    `  00000000-0000-0000-0000-000000000001 - global-management`

  * logs will be like :
    
    
    `
    
        [INFO] consul.acl: ACL bootstrap completed 

        [DEBUG] http: Request PUT /v1/acl/bootstrap (2.347965ms) from=127.0.0.1:40566 
    
    `
      
  
4. All consul request needs token as the argument now. Nothing can happen without acl token passing. 

5. Do this in all servers or agents 

  * `export CONSUL_HTTP_TOKEN=6bac6b50-8df2-7f1d-aa0a-317ebcdd56fa` 

  * Token generated in step 3 will be available to all. And can be verified with  

  * `i.e. Consul members –token “<token_id>”`  

6. To check whether things are done properly or not, one can fire any consul command without passing token_id (in not exported as in point a.), there won’t be any action on fired consul command. Even ‘consul members’ won’t work. 

7. Create agent policy 


  { 

    "key_prefix": { 

      "": { 

        "policy": "read" 

      }, 

      "foo/": { 

        "policy": "write" 

      }, 

      "foo/private/": { 

        "policy": "deny" 

      } 

    }, 

    "key": { 

      "foo/bar/secret": { 

        "policy": "deny" 

      } 

    }, 

    "operator": "read" 

  } 



8. Create agent policy now 

* $ consul acl policy create -name "agent-token" -description "Agent Token Policy" -rules @agent-policy.json 

  <p align="center"><img src="../images/policyCreateImage.PNG?raw=true"></p>
 

9. Create consul agent token and export as given in step 5. 

* consul acl token create -description "Agent Token" -policy-name "agent-token" 

    ` AccessorID:       c39c8299-3502-2bb2-e798-6d67e9ebad98`
    
    ` SecretID:         6fa91881-38c2-8b75-24f2-b5ae32576da2`
    
    ` Description:      Agent Token`
    
    ` Local:            false`
    
    ` Create Time:      2020-07-09 22:59:16.847112371 -0600 MDT`
    
    ` Policies:`
    
    ` 4b06084f-a9dc-63ea-a635-8bd5c16c6c18 - agent-token`
 
   <p align="center"><img src="../images/tokenCreateImage.PNG?raw=true"></p>
 
* `export CONSUL_HTTP_TOKEN=6fa91881-38c2-8b75-24f2-b5ae32576da2`
 
