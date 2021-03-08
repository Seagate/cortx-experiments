CC=/opt/rh/devtoolset-7/root/usr/bin/g++ #use your own path
daospath=/root/src_daos/daos
CFLAGS=-I${daospath}/src/include
LIBDIR=-Lbenchmark/build/src -L${daospath}/install/lib64
LIBS=-pthread -lbenchmark -ldaos -lgurt -ldaos_common -luuid

daos_benchmark : kv_benchmark.cc
        $(CC) -o $@ $^ -std=c++11 -isystem benchmark/include $(CFLAGS) $(LIBDIR) $(LIBS)
