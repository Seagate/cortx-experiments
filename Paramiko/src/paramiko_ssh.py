#!/usr/bin/python3.6

import sys
import paramiko

try:
    action = ["stop", "start", "status", "restart"]
    if len(sys.argv) <= 2 or len(sys.argv) > 3:
        print("usage: %s <start/stop/restart/status> <service-name>\n")
        sys.exit(1)
    if sys.argv[1] not in action:
        print("invalid argument\nusage: %s <start/stop/restart/status> <service-name>\n")
        sys.exit(1)

    action =  sys.argv[1]
    service_name = sys.argv[2]

except Exception as e:
    print(e)

hostname = input("Enter hostname/ip of remote server: ")
username = input ("Enter username: ")

print("Creating SSH client...")
ssh_client = paramiko.SSHClient()

#connect to remote server.
print("Connecting to remote server...")
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#### connect using password
#password = "secret"
#ssh_client.connect(hostname=hostname, username=username, password=password)

### connect using ssh-key
key = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
ssh_client.connect(hostname=hostname, username=username, pkey=key)

# Execute command
command = f"systemctl {action} {service_name}"
print(f"Executing Command: {command} ")
stdin, stdout , stderr = ssh_client.exec_command(command)

# Get return code (0 is default for success)
retcode = stdout.channel.recv_exit_status()
print(f'Return code : {retcode}')
print(f'STDOUT      : {stdout.read().decode("utf8")}')
print(f'STDERR      : {stderr.read().decode("utf8")}')

# close file object
stdin.close()
stdout.close()
stderr.close()

# Close the client
ssh_client.close()
