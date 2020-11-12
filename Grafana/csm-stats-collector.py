# CORTX-CSM: CORTX Management web and CLI interface.
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.

import sys
import traceback
import subprocess
import syslog
import json
import requests
from requests.auth import HTTPBasicAuth
import csv
import argparse
from statsd import StatsClient

class Stats:
    '''' Stats Infrastructure Class '''
    def __init__(self, stats_client):
        self.stats_client = stats_client

class Statsd(Stats):
    ''' Statsd based Infrastructure to push data to statsd '''
    def __init__(self, stats_client):
        Stats.__init__(self, stats_client)

    def count_incr_metric(self, stat, count=1, rate=1):
        self.stats_client.incr(stat, count, rate)

    def count_decr_metric(self, stat, count=1, rate=1):
        self.stats_client.decr(stat, count, rate)

    def time_metric(self, stat, delta, rate=1):
        self.stats_client.timing(stat, delta, rate)

    def gauges_metric(self, stat, value, rate=1, delta=False):
        self.stats_client.gauge(stat, value, rate, delta)

    def sets_metric(self, stat, value, rate=1):
        self.stats_client.set(stat, value, rate)

# Components to Pull data from

class Mero:
    @staticmethod
    def add_args(component_parser):
        parser = component_parser.add_parser("mero",
                    help = "provides mero capacity stats")
        parser.set_defaults(component = Mero)

    @staticmethod
    def handle_stats(stats_client, args):
        ''' Pull mero capacity '''
        try:
            cmd = ['hctl', 'mero', 'status', '--json']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            status_json = json.loads(p.communicate()[0])
            if status_json is None:
                raise Exception("check hctl mero status")
            else:
                total_space = status_json["csrStats"]["_fs_stats"]["_fss_total_disk"]
                free_space = status_json["csrStats"]["_fs_stats"]["_fss_free_disk"]
                used_space = int(total_space) - int(free_space)
                mero = {"mero.total_space": total_space,
                    "mero.free_space": free_space,
                    "mero.used_space": used_space }
                for space in mero:
                    stats_client.gauges_metric(space, mero[space])
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, 'Failed to collect Mero stats: %s. %s' %(e, traceback.format_exc()))

class Haproxy:
    # Keepalived conf file
    KeepalivedConf = "/etc/keepalived/keepalived.conf"

    @staticmethod
    def add_args(component_parser):
        haproxy_parser = component_parser.add_parser("haproxy",
                            help = "provides haproxy backends server stats")
        haproxy_parser.set_defaults(component = Haproxy)
        haproxy_parser.add_argument("node",
                            help = "Select singlenode or multinode.",
                            choices = ["singlenode", "multinode"])
    @staticmethod
    def haproxy_status_check():
        f = open( Haproxy.KeepalivedConf, "r")
        file_content = f.readlines()
        for line in file_content:
            if "interface" in line:
                interface_list = line.split()
                interface = interface_list[interface_list.index("interface") + 1]
            elif "virtual_ipaddress" in line:
                # increment ip index to get next line in file.
                ip_index = file_content.index(line) + 1
                startwith_tup = ("#" , "{")
                while ip_index < len(file_content):
                    ip = file_content[ip_index].split()[0].strip()
                    if not ip.startswith(startwith_tup):
                        break
                    ip_index += 1
        f.close()
        output = subprocess.Popen(["/usr/sbin/ip", "-o", "addr", "list", interface], stdout = subprocess.PIPE)
        var = output.communicate()[0]
        return ip in var

    @staticmethod
    def handle_stats(stats_client, args):
        ''' Pull haroxy backend matrices '''
        try:
            # handle if multinode
            if args.node == "multinode":
                if not Haproxy.haproxy_status_check():
                    return
            url = "http://localhost:8080/stats;csv"
            r = requests.get(url)
            r.raise_for_status()
            data = r.content.lstrip('# ')
            stat_rows = csv.DictReader(data.splitlines())
            for row in stat_rows:
                path = '.'.join(["haproxy", row['pxname'], row['svname']])
                # Report each stat that we want in each row
                for stat in ['econ', 'bin', 'bout', 'hrsp_4xx', 'hrsp_5xx']:
                    val = row.get(stat) or 0
                    stats_client.gauges_metric(path + "." + stat, val)
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, 'Failed to collect Haproxy stats: %s. %s'
                %(e, traceback.format_exc()))

def usage():
    return '''

Collect stats from different component..

component:
    mero
        Info:       It provide mero capacity stats.
        Example:
            $./csm-stats-collector mero

    haproxy
        Info:       It provide haproxy backends server stats.
        Argument:   {singlenode|multinode}
        example:
            $./csm-stats-collector haproxy singlenode
            $./csm-stats-collector haproxy multinode

'''

if __name__ == '__main__':
    try:
        component_dict = { "mero"    : Mero,
                           "haproxy" : Haproxy }

        # Handle invalid component
        if len(sys.argv) < 2:
            raise Exception("Component is not given. %s" %usage())
        elif sys.argv[1] not in component_dict.keys() and sys.argv[1] != "-h":
            raise Exception("Component %s is not valid." %sys.argv[1])

        argParser = argparse.ArgumentParser(
                        usage = "%(prog)s [-h] <component> [<args>]",
                        formatter_class = argparse.RawDescriptionHelpFormatter,
                        description = usage())
        component_parser = argParser.add_subparsers(
                        help = "Select one of given component.")

        for component in component_dict.values():
            component.add_args(component_parser)

        args = argParser.parse_args()
        stats_client = Statsd(StatsClient())
        args.component.handle_stats(stats_client, args)

    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, 'Failed to collect stats: %s. %s' %(e, traceback.format_exc()))
        sys.exit(1)
