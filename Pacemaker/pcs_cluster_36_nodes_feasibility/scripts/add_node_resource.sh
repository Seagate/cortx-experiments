#!/usr/bin/env bash

# Copyright (c) 2020 Seagate Technoechoy LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>. For any questions
# about this software or licensing, please email opensource@seagate.com or
# cortx-questions@seagate.com.

set -eu -o pipefail

pcs resource create motr ocf:seagate:s3server service=motr unique_clone=true clone clone-max=72 clone-node-max=2 globally-unique=true
pcs resource create hax-c1 ocf:heartbeat:Dummy clone op start timeout=50s interval=0s op monitor timeout=50s interval=60s op stop timeout=50s interval=0s

pcs constraint order motr-clone then hax-c1-clone

pcs resource create io_health_path ocf:heartbeat:Dummy clone op start timeout=50s interval=0s op monitor timeout=50s interval=60s op stop timeout=50s interval=0s

pcs constraint  colocation add hax-c1-clone with io_health_path-clone score=INFINITY

pcs resource create haproxy ocf:heartbeat:Dummy clone op start timeout=50s interval=0s op monitor timeout=50s interval=60s op stop timeout=50s interval=0s
pcs resource create s3auth ocf:heartbeat:Dummy clone op start timeout=50s interval=0s op monitor timeout=50s interval=60s op stop timeout=50s interval=0s
pcs resource create s3server ocf:seagate:s3server service=s3server unique_clone=true clone clone-max=396 clone-node-max=11 globally-unique=true

pcs constraint  colocation add s3auth-clone with haproxy-clone score=INFINITY
pcs constraint  colocation add s3server-clone with s3auth-clone score=INFINITY

pcs resource create csm ocf:heartbeat:Dummy op start timeout=50s interval=0s op monitor timeout=50s interval=60s op stop timeout=50s interval=0s
pcs resource create mgmt_health_path ocf:heartbeat:Dummy op start timeout=50s interval=0s op monitor timeout=50s interval=60s op stop timeout=50s interval=0s

pcs constraint  colocation add csm with mgmt_health_path score=INFINITY
