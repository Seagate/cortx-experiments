CC=/opt/rh/devtoolset-7/root/usr/bin/g++ #use your own path
daos_dir=/root/src_daos/daos
benchmark_dir=/root/google_benchmark
CFLAGS=-I$(daos_dir)/src/include
LIBDIR=-L(benchmark_dir)/benchmark/build/src -L${daos_dir}/install/lib64
LIBS=-lpthread -lbenchmark -ldaos -lgurt -ldaos_common -luuid

daos_benchmark : kv_benchmark.cc
        $(CC) -o $@ $^ -std=c++11 -isystem benchmark/include $(CFLAGS) $(LIBDIR) $(LIBS)
