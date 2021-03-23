*   Benchmarking for the daos KV Storage is done using google-benchmark tool. To run this test one needs to install google-benchmark tool on the daos node. Pre-requisites and installation steps are available [here](https://github.com/google/benchmark#requirements).

This directory contains 3 files.

1.  kv_benchmarking.cc
      
    Source file for daos kvs benchmarking test.
    
2.  Makefile 
      
    make file to create the binary(daos_benchmark). Using make command generate the binary and use following command
      
    `$ ./daos_benchmark --benchmark_out=data.json`
      
3.  json_report_to_csv.py
      
    A python script to convert the output json file(data.json) to csv file(benchmark_data_file.csv) using following command.
      
    `$ python3 json_report_to_csv.py`
