import os
import argparse
from runner import Runner
import recover_nodes

def start(playbook, ini):
    return(Runner.run(playbook, ini))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Drive Ansible Runner.')
    parser.add_argument('--ini', type=str, default='/root/inventory')
    parser.add_argument('--playbook', type=str, required=True)
    args = parser.parse_args()

    rc = start(playbook=args.playbook, ini=args.ini)
    if os.path.getsize('/tmp/failed_nodes_ini') > 0:
        print("========================================")
        print("Trying to recover failed Nodes!!!")
        print("========================================")
        recover_nodes.main()
        rc = start(playbook=args.playbook, ini='/tmp/failed_nodes_ini')

