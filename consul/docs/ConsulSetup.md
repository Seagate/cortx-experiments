# Configure consul on system

### Basic configuration

1. Configure Repos
```
yum install -y yum-utils
yum-config-manager --add-repo "${CORTX_RELEASE_REPO}/3rd_party/"
rm -rf /etc/yum.repos.d/*3rd_party*.repo
yum-config-manager --add-repo "${CORTX_RELEASE_REPO}/cortx_iso/"
rm -rf /etc/yum.repos.d/*cortx_iso*.repo
yum clean all
rm -rf /var/cache/yum/
```

2. Install Consul
```
yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
yum -y install consul-1.7.8 --nogpgcheck
```

### Single Node Setup

1. Update systemd file
```
$ vim /usr/lib/systemd/system/consul.service
ExecStart=/usr/bin/consul agent -dev
```

2. Reload Systemd
```
systemctl daemon-reload
```

3. Start service
```
systemctl status consul
systemctl enable consul
systemctl restart consul
```

### Multi Node Configuration

1. Get All Ip
```
<IP-1>
<IP-2>
<IP-3>
```

2. Get Encrypt Key from any one node
  - It will produce key and copy this key as used in configuration.
```
consul keygen
```

3. Update configuration file
    - Update `/etc/consul.d/consul.hcl` file on each node.
```ini
data_dir = "/opt/consul"

client_addr = "0.0.0.0"
bind_addr = "{{ GetInterfaceIP \"eth2\" }}"

ui = true

server = true
bootstrap_expect=3
# Copy encrypt key output from point 2 to below
encrypt = "9ORLhr97vw="
retry_join = ["<IP-1>", "<IP-2>", "<IP-3>"]
```

4. Start consul service on all node
```
systemctl status consul
systemctl enable consul
systemctl restart consul
```

5. Check consul service
```
consul members

Node      Address    Status   Type   Build  Protocol      DC   Segment
node-1  <IP-1>:8301  alive   server  1.7.8      2         dc1   <all>
node-2  <IP-2>:8301  alive   server  1.7.8      2         dc1   <all>
node-3  <IP-3>:8301  alive   server  1.9.4      2         dc1   <all>
```

