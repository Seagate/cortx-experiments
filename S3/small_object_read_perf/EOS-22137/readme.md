# S3bench test run

- Using scripts in "scripts" folder, S3bench tests performed on latest S3 server
codebase (latest as on 1 July 2021) on 'main' branch.
- For S3bench test run, S3 server is set to run in full fake mode on single H/W node cluster
 (node: m24-r29.pun.seagate.com), with single S3 server instance and no 5U84.
- Two configurations are used: 1 client and 40 clients, each with 1Kb object size.
  Refer to scripts "s3bench-*.sh" code in "scripts" folder for more details on parameters
  used to run S3bench tool to generate workload on S3 server.

# addb_db_backup

- This folder contains ADDB databases generated from S3bench test runs and using tools
  from https://github.com/Seagate/seagate-tools.
- Contains raw SQL records (sql_raw*.log) representing S3 requests made by S3bench tool.
  Used below SQL statement to generate raw SQL data:
  "select r.time, r.id, r.pid, s.uuid, r.state from request r INNER JOIN s3_request_uid s ON (r.id = s.id) where type_id="s3_request_state" and r.pid=<S3_PID> Order By r.id ASC;"
  Note: "<S3_PID>" is S3 server PID.
- Script "find_s3_request_time.sh" from "scripts" folder can be used to find time taken by each
  S3 Get Object request made by S3bench tool. It takes raw SQL record file and generates .out file with
  S3 Get Object requests sorted on time taken by the request to complete. 

# scripts
- Folder "scripts" contains shell scripts used in generating various result and intermediate data.

# s3bench_output
- S3bench tool's output is stored in "s3bench_output" folder.

# perf_results
- Histograms generated from ADDB DB stored in folder "addb_db_backup".
- Used tools from https://github.com/Seagate/seagate-tools.
