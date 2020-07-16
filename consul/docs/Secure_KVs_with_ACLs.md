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

    logs will be like :
    
    

      [INFO] consul.acl: ACL bootstrap completed 

      [DEBUG] http: Request PUT /v1/acl/bootstrap (2.347965ms) from=127.0.0.1:40566 
  
      
  
* All consul request needs token as the argument now. Nothing can happen without acl token passing. 

4. Do this in all servers or agents 

  * export CONSUL_HTTP_TOKEN=4411f091-a4c9-48e6-0884-1fcb092da1c8 

  * Token generated in step 3 will be available to all. And can be verified with  

  * i.e. Consul members –token “<token_id>”  

5. To check whether things are done properly or not, one can fire any consul command without passing token_id (in not exported as in point a.), there won’t be any action on fired consul command. Even ‘consul members’ won’t work. 

6. Create agent policy 


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



7. Create agent policy now 

* $ consul acl policy create -name "agent-token" -description "Agent Token Policy" -rules @agent-policy.json 

 

8. Create consul agent token 

* consul acl token create -description "Agent Token" -policy-name "agent-token" 

 

 
