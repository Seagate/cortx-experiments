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

#Script to run single s3bench test
#Options:
#     --numClients $clients --objectSize $objsize --numSamples $clients --sampleReads $((10000 / $clients))

#set -xe
TEST_FOLDER="EOS-22137"

S3BENCH_DIR="/root/s3code/s3bench"
S3_BUILD_DIR="/root/s3code/cortx-s3server"
S3BENCH_ENDPOINT="s3.seagate.com"
S3BENCH_OUTDIR="/var/log/s3bench_out/$TEST_FOLDER"
ADDB_DB_DIR="/var/log/addb_res/$TEST_FOLDER"
num_clients=1
object_size=100b
num_samples=num_clients
test_label="addb_"
sample_reads=$(($num_samples / $num_clients))
tag=dummy

mkdir -p ${S3BENCH_OUTDIR}
mkdir -p ${ADDB_DB_DIR}

if [ $# -eq 0 ]
then
  echo "Please provide command line options"
  exit 1
else
  while [ "$1" != "" ]; do
    case "$1" in
      --numClients )  shift;
                      num_clients=${1};
                      ;;
      --object_size ) shift;
                      object_size=${1};
                      ;;
      --num_samples ) shift;
                      num_samples=${1};
                      ;;
      --sample_reads ) shift;
                      sample_reads=${1};
                      ;;
      --tag_name ) shift;
              tag=${1};
              ;;
      * )
          echo "Invalid argument passed";
          exit 1
          ;;
    esac
    shift
  done
fi

test_label+="c${num_clients}_s${object_size}_cnt${sample_reads}_%d"
echo -e "Running test...${test_label}\n"

cd "${S3_BUILD_DIR}"
echo -e "Step 1. Restart everything...\n"
${S3_BUILD_DIR}/jenkins-build.sh --skip_build --skip_tests --fake_obj --fake_kvs --restart_haproxy

echo -e "Step 2. Run S3bench test...\n"
if [ -f "${S3BENCH_OUTDIR}/s3bench.csv" ]
then
  ${S3BENCH_DIR}/s3bench -endpoint ${S3BENCH_ENDPOINT} -numClients ${num_clients} -numSamples ${num_samples} \
      -objectSize ${object_size} -sampleReads ${sample_reads} -label ${test_label} \
      -o ${S3BENCH_OUTDIR}/s3bench.csv -t "csv+"
else
  ${S3BENCH_DIR}/s3bench -endpoint ${S3BENCH_ENDPOINT} -numClients ${num_clients} -numSamples ${num_samples} \
      -objectSize ${object_size} -sampleReads ${sample_reads} -label ${test_label} \
      -o ${S3BENCH_OUTDIR}/s3bench.csv -t "csv"
fi

# Test directory with ADDB logs
test_dir="c${num_clients}_s${object_size}_cnt${sample_reads}"
mkdir -p ${ADDB_DB_DIR}/${tag}/${test_dir}
rm -rf ${ADDB_DB_DIR}/${tag}/${test_dir}/*

echo -e "Step 3. Stop everything and collect ADDB logs in ${ADDB_DB_DIR}/${tag}/${test_dir} ...\n"
${S3_BUILD_DIR}/jenkins-build.sh --cleanup_only --remove_m0trace --collect_addb "${ADDB_DB_DIR}/${tag}/${test_dir}"

cd -
echo -e "Test run complete for test - ${tag}!!!\n"

exit 0
