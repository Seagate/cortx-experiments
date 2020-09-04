Install Paramiko on local host
* $ pip3 install paramiko

Make sure sshd service up and running
* $ systemctl status sshd

Make sure PasswordAuthentication is yes in /etc/ssh/sshd_config file

Create public and private key using ssh-keygen on local-host.
* $ ssh-keygen

Copy the public key to remote-host using ssh-copy-id
* $ ssh-copy-id -i /root/.ssh/id_rsa.pub remote-host

Execute paramiko_ssh.py script on local-host to start/stop/status/restart service on remote-host
* $ ./paramiko_ssh.py <start/stop/status/restart> <service_name>

- Internally paramiko_ssh.py script uses systemctl to start/stop services. when we execute above cmd internally "systemctl start/stop/restart/status service_name" cmd get executed.

### Test case 1 : start/stop service on remote-host

### Result for successful execution
* Return code = 0
* STDOUT:
* STDERR:

    Example:
    ```
    1. [root@ssc-vm-c-0538 723987]# ./paramiko_ssh.py stop sspl-ll
        Enter hostname/ip of remote server: ssc-vm-c-0208.colo.seagate.com
        Enter username: root
        Creating SSH client...
        Connecting to remote server...
        Executing Command systemctl stop sspl-ll
        Return code: 0
        STDOUT:
        STDERR:
    
    2. [root@ssc-vm-c-0538 723987]# ./paramiko_ssh.py start sspl-ll
        Enter hostname/ip of remote server: ssc-vm-c-0208.colo.seagate.com
        Enter username: root
        Creating SSH client...
        Connecting to remote server...
        Executing Command systemctl start sspl-ll
        Return code: 0
        STDOUT:
        STDERR:

    3. [root@ssc-vm-c-0538 723987]# ./paramiko_ssh.py status sspl-ll
        Enter hostname/ip of remote server: ssc-vm-c-0208.colo.seagate.com
        Enter username: root
        Creating SSH client...
        Connecting to remote server...
        Executing Command systemctl status sspl-ll
        Return code: 0
        STDOUT: ● sspl-ll.service - SSPL Low Level Process
        Loaded: loaded (/etc/systemd/system/sspl-ll.service; enabled; vendor preset: disabled)
        Active: active (running) since Fri 2020-09-04 00:38:11 MDT; 25s ago
        Process: 9238 ExecStopPost=/usr/bin/rm -Rf /var/run/sspl_ll (code=exited, status=0/SUCCESS)
        Process: 11652 ExecStartPre=/usr/bin/chown sspl-ll:root /var/run/sspl_ll (code=exited, status=0/SUCCESS)
        Process: 11650 ExecStartPre=/usr/bin/mkdir -p /var/run/sspl_ll (code=exited, status=0/SUCCESS)
        Process: 11347 ExecStartPre=/opt/seagate/cortx/sspl/bin/sspl_setup check (code=exited, status=0/SUCCESS)
        Main PID: 11655 (sspl_ll_d)
        CGroup: /system.slice/sspl-ll.service
           ├─11655 /usr/bin/sspl_ll_d
           └─11658 /usr/bin/sspl_ll_d

        Sep 04 00:38:07 ssc-vm-c-0539.colo.seagate.com systemd[1]: Starting SSPL Low Level Process...
        Sep 04 00:38:07 ssc-vm-c-0539.colo.seagate.com sudo[11350]:     root : TTY=unknown ; PWD=/ ; USER=root ; COMMAND=/bin/python3 /opt/seagate/cortx/sspl/bin/validate_consul_config.py
        Sep 04 00:38:11 ssc-vm-c-0539.colo.seagate.com systemd[1]: Started SSPL Low Level Process.

        STDERR:


### service failed to start
* Return code : 1
* STDOUT      :
* STDERR      : Job for rabbitmq-server.service failed because the control process exited with error code. See "systemctl status rabbitmq-server.service" and "journalctl -xe" for details.

    Example:
    ```
    1. [root@ssc-vm-c-0538 723987]# ./paramiko_ssh.py start rabbitmq-server
        Enter hostname/ip of remote server: ssc-vm-c-0539.colo.seagate.com
        Enter username: root
        Creating SSH client...
        Connecting to remote server...
        Executing Command: systemctl start rabbitmq-server
        Return code : 1
        STDOUT      :
        STDERR      : Job for rabbitmq-server.service failed because the control process exited with error code. See "systemctl status rabbitmq-server.service" and "journalctl -xe" for details.

    2. [root@ssc-vm-c-0538 723987]# ./paramiko_ssh.py status rabbitmq-server
        Enter hostname/ip of remote server: ssc-vm-c-0539.colo.seagate.com
        Enter username: root
        Creating SSH client...
        Connecting to remote server...
        Executing Command: systemctl status rabbitmq-server
        Return code : 3
        STDOUT      : ● rabbitmq-server.service - RabbitMQ broker
        Loaded: loaded (/usr/lib/systemd/system/rabbitmq-server.service; disabled; vendor preset: disabled)
        Active: failed (Result: exit-code) since Fri 2020-09-04 06:21:53 MDT; 13min ago
        Process: 3356 ExecStart=/usr/lib/rabbitmq/bin/rabbitmq-server (code=exited, status=200/CHDIR)
        Main PID: 3356 (code=exited, status=200/CHDIR)

        Sep 04 06:21:50 ssc-vm-c-0539.colo.seagate.com systemd[1]: Starting RabbitMQ broker...
        Sep 04 06:21:53 ssc-vm-c-0539.colo.seagate.com systemd[1]: rabbitmq-server.service: main process exited, code=exited, status=200/CHDIR
        Sep 04 06:21:53 ssc-vm-c-0539.colo.seagate.com systemd[1]: Failed to start RabbitMQ broker.
        Sep 04 06:21:53 ssc-vm-c-0539.colo.seagate.com systemd[1]: Unit rabbitmq-server.service entered failed state.
        Sep 04 06:21:53 ssc-vm-c-0539.colo.seagate.com systemd[1]: rabbitmq-server.service failed.

        STDERR      :


### Test case 2 : Start/stop Invalid service.
Ex. : systemctl start/stop abcd
* Return code : 5
* STDOUT      :
* STDERR      : Failed to stop abcd.service: Unit abcd.service not loaded.

    Example:
    ```
    1. [root@ssc-vm-c-0538 723987]# ./paramiko_ssh.py stop abcd
        Enter hostname/ip of remote server: ssc-vm-c-0208.colo.seagate.com
        Enter username: root
        Creating SSH client...
        Connecting to remote server...
        Executing Command: systemctl stop abcd
        Return code : 5
        STDOUT      :
        STDERR      : Failed to stop abcd.service: Unit abcd.service not loaded.


    2. [root@ssc-vm-c-0538 723987]# ./paramiko_ssh.py status abcd
        Enter hostname/ip of remote server: ssc-vm-c-0208.colo.seagate.com
        Enter username: root
        Creating SSH client...
        Connecting to remote server...
        Executing Command systemctl status abcd
        Return code: 4
        STDOUT:
        STDERR: Unit abcd.service could not be found.

