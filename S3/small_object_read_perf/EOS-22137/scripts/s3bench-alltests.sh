#!/bin/sh
#
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.
#

#Script to run collection of s3bench tests
#set -xe
echo -e "Running all S3bench tests...\n"
for iter in {1..5}; do
  echo -e "Running test for obj size=1Kb and clients=40 ...\n"
  ./s3bench-single-test.sh --numClients 40 --object_size 1Kb --num_samples 40 --sample_reads 1000 --tag_name "test$iter"
done
