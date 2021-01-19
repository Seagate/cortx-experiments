#awk '{print $NF}' /etc/hosts > /tmp/nodelist

cat /tmp/nodelist | xargs -I %REPL ssh root@%REPL "mkdir -p /usr/lib/systemd/system/ ; mkdir -p /usr/lib/ocf/resource.d/seagate/ ;";

cat /tmp/nodelist | xargs -I %REPL scp s3server-service root@%REPL:/root/s3server-service
cat /tmp/nodelist | xargs -I %REPL scp s3server root@%REPL:/usr/lib/ocf/resource.d/seagate/
cat /tmp/nodelist | xargs -I %REPL scp s3server@.service root@%REPL:/usr/lib/systemd/system/
cat /tmp/nodelist | xargs -I %REPL scp motr@.service root@%REPL:/usr/lib/systemd/system/
cat /tmp/nodelist | xargs -I %REPL scp pass root@%REPL:/root/pass


cat /tmp/nodelist | xargs -I %REPL ssh root@%REPL "systemctl daemon-reload"

