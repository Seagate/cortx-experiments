# demo file

/**
 * Benchmarking tests for cortx-motr kv store.
 * Operation type    : put, get, list, remove.
 * Operation number   : NR_OPS_XXXX per each operation
 */

#include <benchmark/benchmark.h>

#include <cstdio>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include <math.h>
#include <sys/stat.h>

#include "lib/memory.h"
#include "lib/types.h"
#include "motr/client.h"
#include "motr/idx.h" //TODO

/* number of operations */
#define NR_OPS_100     100
#define NR_OPS_1000    1000
#define NR_OPS_10000   10000
#define NR_OPS_100000  100000
#define NR_OPS_1000000 1000000

/* number of query at a time while listing */
#define NR_KV_PER_LISTING 8

/* key sizes */
#define BM_KEY_64B   64
#define BM_KEY_128B  128
#define BM_KEY_256B  256
#define BM_KEY_512B  512
#define BM_KEY_1024B 1024

/* value sizes */
#define BM_VAL_1K  1024
#define BM_VAL_4K  (1024 * 4)
#define BM_VAL_8K  (1024 * 8)
#define BM_VAL_16K (1024 * 16)
#define BM_VAL_32K (1024 * 32)

/* buffer to hold keys while listing */
#define KEY_LIST_BUF (1024 * 1024)

#define ARG_KEY_SIZE_OPTIONS { BM_KEY_64B , BM_KEY_128B, BM_KEY_256B, BM_KEY_512B, BM_KEY_1024B }
#define ARG_VAL_SIZE_OPTIONS { BM_VAL_1K , BM_VAL_4K, BM_VAL_8K, BM_VAL_16K, BM_VAL_32K  }
#define NR_OPS_OPTIONS       { /*NR_OPS_100, NR_OPS_1000,*/ NR_OPS_10000 /*, NR_OPS_100000, NR_OPS_1000000*/ } //default ops are set to 10k by default

#define KEY_STR_SIZE 16

#define ARG_MATRICS\
   { ARG_KEY_SIZE_OPTIONS, ARG_VAL_SIZE_OPTIONS, NR_OPS_OPTIONS }

#define DEBUG_LOG 0

#if DEBUG_LOG
#define LOG_MSG printf
#else
#define LOG_MSG //
#endif

static daos_handle_t poh; /* daos pool handle */
static daos_handle_t coh; /* daos container handle */

static char err_msg[ 128 ];

#define FAIL( fmt, ... )                                            \
    do {                                                            \
        fprintf(stderr, "Process (%s): " fmt " aborting\n",         \
                err_msg, ## __VA_ARGS__);                           \
        exit(1);                                                    \
    } while (0)

#define ASSERT( cond, ... )                                         \
    do {                                                            \
        if (!(cond))                                                \
        FAIL(__VA_ARGS__);                                          \
    } while (0)

daos_handle_t oh;  /* object handle */
daos_obj_id_t oid; /* daos object id */

uuid_t pool_uuid; /* pool uuid */
uuid_t co_uuid;   /* container uuid */

#include <gflags/gflags.h>
#include <inttypes.h>

//TBD add params gflag

/* Motr parameters */

DEFINE_string( action, "none",
               "KVS action:get,next,put,del,createidx,deleteidx" );
DEFINE_string( op_oid, "", "KVS operation oid" );
DEFINE_string( key, "", "KVS operation key" );
DEFINE_string( value, "", "KVS operation value" );
DEFINE_int32( op_count, 10, "number of keys" );
DEFINE_string( index_hi, "", "KVS operation oid HI <0xhex64bitOidString>" );
DEFINE_string( index_lo, "", "KVS operation oid LO <0xhex64bitOidString>" );
DEFINE_int32( kvstore, 2, "Type of index service: 1:MOTR; 2:CASSANDRA" );

DEFINE_string( motr_local_addr, "local@tcp:12345:33:100", "Motr local address" );
DEFINE_string( motr_ha_addr, "local@tcp:12345:34:1", "Motr ha address" );
DEFINE_string( motr_profile, "<0x7000000000000001:0>", "Motr profile" );
DEFINE_string( motr_proc, "<0x7200000000000000:0>", "Motr proc" );
DEFINE_string( motr_kvs_keyspace, "motr_index_keyspace", "Motr keyspace" );
DEFINE_string( motr_cluster_ep, "127.0.0.1", "Cluster EP" );
DEFINE_int32( recv_queue_min_len, 16,
              "Recv Queue min length: default 16" ); // As Suggested by Motr team
DEFINE_int32( max_rpc_msg_size, 65536,
              "RPC msg size max: default 65536" ); // As Suggested by Motr team

static struct m0_idx_dix_config  dix_conf;
static struct m0_idx_cass_config cass_conf;
static struct m0_client          *motr_instance = NULL;
static struct m0_container       motr_container;
static struct m0_realm           motr_uber_realm;
static struct m0_config          motr_conf;

struct m0_uint128 root_user_index_oid;
struct m0_uint128 root_user_bucket_list_oid;

struct m0_uint128 id; // this could be global //TBD

id.u_hi = std::stoull( FLAGS_index_hi, nullptr, 0 );
id.u_lo = std::stoull( FLAGS_index_lo, nullptr, 0 );

static int init_motr( void ) {
   int rc;

   motr_conf.mc_is_oostore            = true;
   motr_conf.mc_is_read_verify        = false;
   motr_conf.mc_local_addr            = FLAGS_motr_local_addr.c_str( );
   motr_conf.mc_ha_addr               = FLAGS_motr_ha_addr.c_str( );
   motr_conf.mc_profile               = FLAGS_motr_profile.c_str( );
   motr_conf.mc_process_fid           = FLAGS_motr_proc.c_str( );
   motr_conf.mc_tm_recv_queue_min_len = FLAGS_recv_queue_min_len;
   motr_conf.mc_max_rpc_msg_size      = FLAGS_max_rpc_msg_size;

   cass_conf.cc_cluster_ep = const_cast<char *>( FLAGS_motr_cluster_ep.c_str( ) );
   cass_conf.cc_keyspace   = const_cast<char *>( FLAGS_motr_kvs_keyspace.c_str( ) );

   cass_conf.cc_max_column_family_num = 1;
   dix_conf.kc_create_meta            = false;
   motr_conf.mc_idx_service_id        = FLAGS_kvstore;

   if ( FLAGS_kvstore == 2 )
      motr_conf.mc_idx_service_conf = &cass_conf;
   else
      motr_conf.mc_idx_service_conf = &dix_conf;

   motr_conf.mc_layout_id = 0;

   /* Motr instance */
   rc = m0_client_init( &motr_instance, &motr_conf, true );

   if ( rc != 0 )
   {
      fprintf( stderr, "Failed to initilise Motr\n" );
      goto err_exit;
   }

   /* And finally, motr root realm */
   m0_container_init( &motr_container, NULL, &M0_UBER_REALM, motr_instance );

   motr_uber_realm = motr_container.co_realm;

   return 0;

err_exit:

   return rc;
}

int setup_main( &argc, &argv )
{
   int rc;

   // Get input parameters

   gflags::ParseCommandLineFlags( &argc, &argv, false );

   rc = init_motr( );

   if ( rc < 0 )
   {
      return rc;
   }

   id.u_hi = std::stoull( FLAGS_index_hi, nullptr, 0 ); // set id
   id.u_lo = std::stoull( FLAGS_index_lo, nullptr, 0 ); // set id
}

void tear_down( ) {
   m0_client_fini( motr_instance, true );
}

static void idx_bufvec_free( struct m0_bufvec *bv ) {
   uint32_t i;

   if ( bv == NULL )
      return;

   if ( bv->ov_buf != NULL )
   {
      for ( i = 0; i < bv->ov_vec.v_nr; ++i )
         free( bv->ov_buf[ i ] );

      free( bv->ov_buf );
   }

   free( bv->ov_vec.v_count );
   free( bv );
}

static struct m0_bufvec *idx_bufvec_alloc( int nr )
{
   struct m0_bufvec *bv;

   bv = ( m0_bufvec * )m0_alloc( sizeof( *bv ) );

   if ( bv == NULL )
      return NULL;

   bv->ov_vec.v_nr    = nr;
   bv->ov_vec.v_count = ( m0_bcount_t * )calloc( nr, sizeof( bv->ov_vec.v_count[ 0 ] ) );

   if ( bv->ov_vec.v_count == NULL )
      goto FAIL;

   bv->ov_buf = ( void ** )calloc( nr, sizeof( bv->ov_buf[ 0 ] ) );

   if ( bv->ov_buf == NULL )
      goto FAIL;

   return bv;

FAIL:

   if ( bv != NULL && bv->ov_vec.v_count != NULL )
   {
      free( bv->ov_vec.v_count );
   }

   m0_bufvec_free( bv );

   return NULL;
}

void gen_key_name( char *key_buf, int nr, int key_size )
{
   char key_name[ 20 ] = {
      0
   };

   unsigned int key_buf_len = key_size - 1;

   /* generate different key */
   memset( key_buf, 'x', key_buf_len );
   sprintf( key_name, "%.16d", nr ); // variable part of key_name is KEY_STR_SIZE(16) Bytes long
   memcpy( ( char * )key_buf + key_buf_len - KEY_STR_SIZE, ( char * )key_name, KEY_STR_SIZE );
}

static void kv_put_function( benchmark::State &state )
{
   int              rc = 0;
   struct m0_bufvec *keys;
   struct m0_bufvec *vals;
   int              rc_key = 0;

   int          key_size = state.range( 0 ); //param form gb
   int          val_size = state.range( 1 ); // param from gb
   unsigned int num_ops  = state.range( 2 ); // num_ops is number of key-value pairs for the given test

   /* allocate key and value buffers */
   // key buffer allocated
   char *key_buf = ( char * )calloc( key_size, sizeof( char ) );

   ASSERT( key_buf != NULL, "failed to allocate memory" );

   // value buffer allocated
   char *val_buf = ( char * )calloc( val_size, sizeof( char ) );
   ASSERT( val_buf != NULL, "failed to allocate memory" );
   memset( val_buf, 'z', val_size - 1 ); // populate with some random value.

   for ( auto _ : state )
   {
      state.PauseTiming( );

      /* Allocate bufvec's for keys and vals. */
      keys = idx_bufvec_alloc( 1 );
      vals = idx_bufvec_alloc( 1 );

      if ( keys == NULL || vals == NULL )
      {
         rc = -ENOMEM;
         fprintf( stderr, "Memory allocation failed:%d\n", rc );
         goto ERROR;
      }

      // allocate for various key size and buf sizes.
      keys->ov_vec.v_count[ 0 ] = key_size;
      keys->ov_buf[ 0 ]         = m0_alloc( key_size );

      if ( keys->ov_buf[ 0 ] == NULL )
         goto ERROR;

      vals->ov_vec.v_count[ 0 ] = val_size;
      vals->ov_buf[ 0 ]         = ( char * )malloc( val_size ); // does it contain NULL termination or not
      memcpy( vals->ov_buf[ 0 ], val_buf, val_size );           // fix

      for ( int i = 0; i < num_ops; i++ )
      {
         // gen key here
         gen_key_name( key_buf, i, key_size ); //TBD

         memcpy( keys->ov_buf[ 0 ], key_buf, key_size );

         // execute call comes here. //TBD
         {
            int           rc;
            struct m0_op  *ops[ 1 ] = {
               NULL
            };
            struct m0_idx idx;

            memset( &idx, 0, sizeof( idx ) );
            ops[ 0 ] = NULL;

            m0_idx_init( &idx, &motr_uber_realm, &id ); //id is global, key_name would be generated, valbuf will be generated once.
            m0_idx_op( &idx, M0_IC_PUT, keys, vals, &rc_key, 0, &ops[ 0 ] );

            state.startTiming( );
            // actual timing comes here
            m0_op_launch( ops, 1 );
            rc = m0_op_wait( ops[ 0 ], M0_BITS( M0_OS_FAILED, M0_OS_STABLE ), M0_TIME_NEVER );
            // timing stops
            state.PauseTiming( );

            if ( rc < 0 || rc_key < 0 )
            {
               fprintf( stderr, "Motr op failed:%d \n", rc );
               goto ERROR;
            }

            rc = m0_rc( ops[ 0 ] ); // can be ignored

            /* fini and release */
            m0_op_fini( ops[ 0 ] );
            m0_op_free( ops[ 0 ] );
            m0_entity_fini( &idx.in_entity );
         }
      }
   } // TBDD

ERROR:

   if ( keys )
      idx_bufvec_free( keys );

   if ( vals )
      idx_bufvec_free( vals );

   return rc;
}

/* Benchmarking function to test KV Get operation */
static void kv_get_function( benchmark::State &state ) {
   int              rc = 0;
   struct m0_bufvec *keys;
   struct m0_bufvec *vals;
   int              rc_key = 0;

   int key_size = state.range( 0 ); //param form gb
   //int          val_size = state.range( 1 ); // param from gb
   unsigned int num_ops = state.range( 2 ); // num_ops is number of key-value pairs for the given test

   /* allocate key and value buffers */
   // key buffer allocated
   char *key_buf = ( char * )calloc( key_size, sizeof( char ) );

   ASSERT( key_buf != NULL, "failed to allocate memory" );

   for ( auto _ : state )
   {
      state.PauseTiming( );

      /* Allocate bufvec's for keys and vals. */
      keys = idx_bufvec_alloc( 1 );
      vals = idx_bufvec_alloc( 1 );

      if ( keys == NULL || vals == NULL )
      {
         rc = -ENOMEM;
         fprintf( stderr, "Memory allocation failed:%d\n", rc );
         goto ERROR;
      }

      // allocate for various key size and buf sizes.
      keys->ov_vec.v_count[ 0 ] = key_size - 1; // TBDD it should be less than 1
      keys->ov_buf[ 0 ]         = m0_alloc( key_size );

      if ( keys->ov_buf[ 0 ] == NULL )
         goto ERROR;

      for ( int i = 0; i < num_ops; i++ )
      {
         // gen key here
         gen_key_name( key_buf, i, key_size ); //TBD

         memcpy( keys->ov_buf[ 0 ], key_buf, key_size );

         // execute call comes here. //TBD
         {
            int           rc;
            struct m0_op  *ops[ 1 ] = {
               NULL
            };
            struct m0_idx idx;

            memset( &idx, 0, sizeof( idx ) );
            ops[ 0 ] = NULL;

            m0_idx_init( &idx, &motr_uber_realm, &id ); //id is global, key_name would be generated, valbuf will be generated once.
            m0_idx_op( &idx, M0_IC_GET, keys, vals, &rc_key, 0, &ops[ 0 ] );

            state.startTiming( );
            // actual timing comes here
            m0_op_launch( ops, 1 );
            rc = m0_op_wait( ops[ 0 ], M0_BITS( M0_OS_FAILED, M0_OS_STABLE ), M0_TIME_NEVER );
            // timing stops
            state.PauseTiming( );

            if ( rc < 0 || rc_key < 0 )
            {
               fprintf( stderr, "Motr op failed:%d \n", rc );
               goto ERROR;
            }

            rc = m0_rc( ops[ 0 ] ); // can be ignored

            /* fini and release */
            m0_op_fini( ops[ 0 ] );
            m0_op_free( ops[ 0 ] );
            m0_entity_fini( &idx.in_entity );
         }

         if ( keys->ov_buf[ 0 ] == NULL )
            goto ERROR;

         fprintf( stdout, "Index:%" PRIx64 ":%" PRIx64 "\n", id.u_hi, id.u_lo );
         fprintf( stdout, "Key: %.*s\n", ( int )keys->ov_vec.v_count[ 0 ],
                  ( char * )keys->ov_buf[ 0 ] );

         if ( vals->ov_buf[ 0 ] == NULL )
         {
            fprintf( stdout, "Val: \n" );
         }
         else
         {
            fprintf( stdout, "Val: %.*s\n", ( int )vals->ov_vec.v_count[ 0 ],
                     ( char * )vals->ov_buf[ 0 ] );
         }

         fprintf( stdout, "----------------------------------------------\n" );
      }
   }

ERROR:

   if ( keys )
      idx_bufvec_free( keys );

   if ( vals )
      idx_bufvec_free( vals );

   return rc;
}

/* Benchmarking function to test KV List operation */
static void kv_list_function( benchmark::State &state ) {
   int              rc = 0;
   struct m0_bufvec *keys;
   struct m0_bufvec *vals;
   int              *rc_key = NULL;

   int          key_size = state.range( 0 ); //param form gb
   int          val_size = state.range( 1 ); // param from gb
   unsigned int num_ops  = state.range( 2 ); // num_ops is number of key-value pairs for the given test
   unsigned int nr_kvp   = NR_KVP_PER_FETCH; // TBDD

   /* allocate key and value buffers */
   // key buffer allocated
   char *key_buf = ( char * )calloc( key_size, sizeof( char ) );

   ASSERT( key_buf != NULL, "failed to allocate memory" );

   // value buffer allocated
   char *val_buf = ( char * )calloc( val_size, sizeof( char ) );
   ASSERT( val_buf != NULL, "failed to allocate memory" );
   memset( val_buf, 'z', val_size - 1 ); // populate with some random value.

   for ( auto _ : state )
   {
      state.PauseTiming( );

      /* Allocate bufvec's for keys and vals. */
      /* Allocate bufvec's for keys and vals. */
      keys    = idx_bufvec_alloc( nr_kvp );
      vals    = idx_bufvec_alloc( nr_kvp );
      rc_keys = ( int * )calloc( nr_kvp, sizeof( int ) );

      if ( keys == NULL || vals == NULL || rc_keys == NULL )
      {
         rc = -ENOMEM;
         fprintf( stderr, "Memory allocation failed:%d\n", rc );
         goto ERROR;
      }

      if ( keys == NULL || vals == NULL )
      {
         rc = -ENOMEM;
         fprintf( stderr, "Memory allocation failed:%d\n", rc );
         goto ERROR;
      }

      // allocate for various key size and buf sizes.
      keys->ov_vec.v_count[ 0 ] = key_size;
      keys->ov_buf[ 0 ]         = m0_alloc( key_size );

      if ( keys->ov_buf[ 0 ] == NULL )
         goto ERROR;

      vals->ov_vec.v_count[ 0 ] = val_size;
      vals->ov_buf[ 0 ]         = ( char * )malloc( val_size ); // does it contain NULL termination or not
      memcpy( vals->ov_buf[ 0 ], val_buf, val_size );           // fix

      for ( int i = 0; i < num_ops; i++ )
      {
         // gen key here
         gen_key_name( key_buf, i, key_size ); //TBD

         memcpy( keys->ov_buf[ 0 ], key_buf, key_size );

         // execute call comes here. //TBD
         {
            int           rc;
            struct m0_op  *ops[ 1 ] = {
               NULL
            };
            struct m0_idx idx;

            memset( &idx, 0, sizeof( idx ) );
            ops[ 0 ] = NULL;

            m0_idx_init( &idx, &motr_uber_realm, &id ); //id is global, key_name would be generated, valbuf will be generated once.
            m0_idx_op( &idx, M0_IC_PUT, keys, vals, &rc_key, 0, &ops[ 0 ] );

            state.startTiming( );
            // actual timing comes here
            m0_op_launch( ops, 1 );
            rc = m0_op_wait( ops[ 0 ], M0_BITS( M0_OS_FAILED, M0_OS_STABLE ), M0_TIME_NEVER );
            // timing stops
            state.PauseTiming( );

            if ( rc < 0 || rc_key < 0 )
            {
               fprintf( stderr, "Motr op failed:%d \n", rc );
               goto ERROR;
            }

            rc = m0_rc( ops[ 0 ] ); // can be ignored

            /* fini and release */
            m0_op_fini( ops[ 0 ] );
            m0_op_free( ops[ 0 ] );
            m0_entity_fini( &idx.in_entity );
         }
      }
   } // TBDD

ERROR:

   if ( keys )
      idx_bufvec_free( keys );

   if ( vals )
      idx_bufvec_free( vals );

   return rc;
}

/* Benchmarking function to test KV Remove operation */
static void kv_delete_function( benchmark::State &state ) {
   int              rc = 0;
   struct m0_bufvec *keys;
   struct m0_bufvec *vals  = NULL;
   int              rc_key = 0;

   int          key_size = state.range( 0 ); //param form gb
   unsigned int num_ops  = state.range( 2 ); // num_ops is number of key-value pairs for the given test

   /* allocate key and value buffers */
   // key buffer allocated
   char *key_buf = ( char * )calloc( key_size, sizeof( char ) );

   ASSERT( key_buf != NULL, "failed to allocate memory" );

   for ( auto _ : state )
   {
      state.PauseTiming( );

      /* Allocate bufvec's for keys and vals. */
      keys = idx_bufvec_alloc( 1 );

      if ( keys == NULL )
      {
         rc = -ENOMEM;
         fprintf( stderr, "Memory allocation failed:%d\n", rc );
         goto ERROR;
      }

      // allocate for various key size and buf sizes.
      keys->ov_vec.v_count[ 0 ] = key_size - 1; // TBDD it should be less than 1
      keys->ov_buf[ 0 ]         = m0_alloc( key_size );

      if ( keys->ov_buf[ 0 ] == NULL )
         goto ERROR;

      for ( int i = 0; i < num_ops; i++ )
      {
         // gen key here
         gen_key_name( key_buf, i, key_size ); //TBD

         memcpy( keys->ov_buf[ 0 ], key_buf, key_size - 1 );

         // execute call comes here. //TBD
         {
            int           rc;
            struct m0_op  *ops[ 1 ] = {
               NULL
            };
            struct m0_idx idx;

            memset( &idx, 0, sizeof( idx ) );
            ops[ 0 ] = NULL;

            m0_idx_init( &idx, &motr_uber_realm, &id ); //id is global, key_name would be generated, valbuf will be generated once.
            m0_idx_op( &idx, M0_IC_DEL, keys, vals, &rc_key, 0, &ops[ 0 ] );

            state.startTiming( );
            // actual timing comes here
            m0_op_launch( ops, 1 );
            rc = m0_op_wait( ops[ 0 ], M0_BITS( M0_OS_FAILED, M0_OS_STABLE ), M0_TIME_NEVER );
            // timing stops
            state.PauseTiming( );

            if ( rc < 0 || rc_key < 0 )
            {
               fprintf( stderr, "Motr op failed:%d \n", rc );
               goto ERROR;
            }

            rc = m0_rc( ops[ 0 ] ); // can be ignored

            /* fini and release */
            m0_op_fini( ops[ 0 ] );
            m0_op_free( ops[ 0 ] );
            m0_entity_fini( &idx.in_entity );
         }

         if ( rc < 0 || rc_key < 0 )
         {
            fprintf( stderr, "Index Operation failed:%d\n", rc );
            goto ERROR;
         }

         fprintf( stdout, "Index:%" PRIx64 ":%" PRIx64 "\n", id.u_hi, id.u_lo );
         fprintf( stdout, "Key: %.*s\n", ( int )keys->ov_vec.v_count[ 0 ],
                  ( char * )keys->ov_buf[ 0 ] );
         fprintf( stdout, "successfully deleted \n" );
         fprintf( stdout, "----------------------------------------------\n" );

         fprintf( stdout, "----------------------------------------------\n" );

         idx_bufvec_free( keys );
         idx_bufvec_free( vals ); //TBDD
      }
   }

ERROR:

   if ( keys )
      idx_bufvec_free( keys );

   if ( vals )
      idx_bufvec_free( vals );

   return rc;
}

/* Put keys */
BENCHMARK( kv_put_function )
->ArgsProduct( ARG_MATRICS )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

/* Get keys */
BENCHMARK( kv_get_function )
->ArgsProduct( ARG_MATRICS )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

/* list keys */
BENCHMARK( kv_list_function )
->ArgsProduct( ARG_MATRICS )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

/* remove keys */
BENCHMARK( kv_delete_function )
->ArgsProduct( ARG_MATRICS )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

/* Run the benchmark */
BENCHMARK_MAIN( );
