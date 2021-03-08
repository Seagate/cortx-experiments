/**
 * Example kv store
 */
#include <benchmark/benchmark.h>
#include <cstdio>
#include <daos.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#define POOL_ID "7d630b52-65c3-4061-aa87-4e02b4e6d818"

/* number of keys */
#define NR_KEYS_100    100
#define NR_KEYS_1000   1000
#define NR_KEYS_10000  10000
#define NR_KEYS_100000 100000

/* number of query at a time while listing */
#define NR_QUERY 10

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
#define KEY_DESC_BUF (1024 * 1024)

static char node[ 128 ] = "new_node";

static daos_handle_t poh;
static daos_handle_t coh;

#define FAIL( fmt, ... )                                            \
    do {                                                            \
        fprintf(stderr, "Process (%s): " fmt " aborting\n",         \
                node, ## __VA_ARGS__);                              \
        exit(1);                                                    \
    } while (0)

#define ASSERT( cond, ... )                                         \
    do {                                                            \
        if (!(cond))                                                \
        FAIL(__VA_ARGS__);                                          \
    } while (0)

#define BUFLEN 100

daos_handle_t oh;
daos_obj_id_t oid;
int           rc;

uuid_t pool_uuid, co_uuid;

int setup_main( )
{
   /** initialize DAOS by connecting to local agent */
   rc = daos_init( );
   ASSERT( rc == 0, "daos_init failed with %d", rc );

   rc = uuid_parse( POOL_ID, pool_uuid );

   rc = daos_pool_connect( pool_uuid, NULL, DAOS_PC_RW, &poh,
                           NULL, NULL );
   ASSERT( rc == 0, "pool connect failed with %d", rc );

   /** generate uuid for container */
   uuid_generate( co_uuid );

   /** create container */
   rc = daos_cont_create( poh, co_uuid, NULL /* properties */,
                          NULL /* event */ );
   ASSERT( rc == 0, "container create failed with %d", rc );

   /** open container */
   rc = daos_cont_open( poh, co_uuid, DAOS_COO_RW, &coh, NULL,
                        NULL );
   ASSERT( rc == 0, "container open failed with %d", rc );

   /** share container handle with peer tasks */

   oid.hi = 0;
   oid.lo = 4;

   /** the KV API requires the flat feature flag be set in the oid */
   daos_obj_generate_id( &oid, DAOS_OF_KV_FLAT, OC_SX, 0 );

   rc = daos_kv_open( coh, oid, DAOS_OO_RW, &oh, NULL );
   ASSERT( rc == 0, "KV open failed with %d", rc );
}

void tear_down( ) {
   //close object handle
   daos_kv_close( oh, NULL );

   rc = daos_cont_close( coh, NULL );
   ASSERT( rc == 0, "cont close failed" );

   rc = daos_pool_disconnect( poh, NULL );
   ASSERT( rc == 0, "disconnect failed" );

   /** teardown the DAOS stack */
   rc = daos_fini( );
   ASSERT( rc == 0, "daos_fini failed with %d", rc );
}

// bnechmark function is getting called here.
static void kv_remove_function( benchmark::State &state ) {
   /* perform setup */
   setup_main( );

   char key_name[ 20 ] = {
      0
   };

   unsigned int key_size = state.range( 0 );
   unsigned int val_size = state.range( 1 );
   unsigned int num_keys = state.range( 2 );

   /* allocate key and value buffers */
   char *key_buf = ( char * )calloc( key_size, sizeof( char ) ); // key buffer allocated

   /* actual computation starts here */
   for ( auto _ : state )
   {
      /* call daos_kv_put for state.range(2) times */
      for ( int i = 0; i < num_keys; i++ )
      {
         state.PauseTiming( );

         /* generate different key */
         memset( key_buf, 'x', key_size - 1 );
         sprintf( key_name, "%d", i );
         strncpy( ( char * )key_buf + strlen( key_buf ) - strlen( key_name ), ( char * )key_name, strlen( key_name ) );

         state.ResumeTiming( );

         /* actual function to mearsure time */
         daos_kv_remove( oh, DAOS_TX_NONE, 0, key_buf, NULL );
      }
   }

   /* free resources */
   free( key_buf );

   /* tear down */
   tear_down( );
}

// bnechmark function is getting called here.
static void kv_list_function( benchmark::State &state ) {
   /* perform setup */
   setup_main( );

   char key_name[ 20 ] = {
      0
   };

   unsigned int key_size = state.range( 0 );
   unsigned int val_size = state.range( 1 );
   unsigned int num_keys = state.range( 2 );
   unsigned int nr_query = state.range( 3 );

   /* allocate key and value buffers */
   char *key_buf = ( char * )calloc( key_size, sizeof( char ) ); // key buffer allocated
   char *val_buf = ( char * )calloc( val_size, sizeof( char ) ); // value buffer allocated
   memset( val_buf, 'z', val_size - 1 );                         // populate with some random value.

   char *rbuf = ( char * )calloc( val_size, sizeof( char ) ); // rbuf to check value

   /* call daos_kv_put for state.range(2) times */
   for ( int i = 0; i < num_keys; i++ )
   {
      /* generate different key */
      memset( key_buf, 'x', key_size - 1 );
      sprintf( key_name, "%d", i );
      strncpy( ( char * )key_buf + strlen( key_buf ) - strlen( key_name ), ( char * )key_name, strlen( key_name ) );

      /* put keys and values */
      daos_kv_put( oh, DAOS_TX_NONE, 0, ( char * )key_buf, val_size, val_buf, NULL );
   }

   /* actual computation starts here */
   for ( auto _ : state )
   {
      state.PauseTiming( );
       
      char            *buf;
      daos_key_desc_t kds[ NR_QUERY ];
      daos_anchor_t   anchor = {
         0
      };
      int             key_nr = 0;
      d_sg_list_t     sgl;
      d_iov_t         sg_iov;

      buf = ( char * )calloc( KEY_DESC_BUF, sizeof( char ) );
      d_iov_set( &sg_iov, buf, KEY_DESC_BUF );
      sgl.sg_nr     = 1;
      sgl.sg_nr_out = 0;
      sgl.sg_iovs   = &sg_iov;
       
      state.ResumeTiming( );

      while ( !daos_anchor_is_eof( &anchor ) )
      {
         uint32_t nr = NR_QUERY;
         int      rc;

         memset( buf, 0, KEY_DESC_BUF );

         rc = daos_kv_list( oh, DAOS_TX_NONE, &nr, kds, &sgl, &anchor, \
                            NULL );
         ASSERT( rc == 0, "KV list failed with %d", rc );

         /* verify if returned number of descriptors are zero */
         if ( nr == 0 )
         {
            continue;
         }
         else // if returned descriptors are non zero then compute each key and query value.
         {
            unsigned int offset = 0;

            /* compute each key and fetch value */
            for ( int i = 0; i < nr; i++ )
            {
               memset( key_buf, 0, key_size );
               memset( rbuf, 0, val_size );

               /* obtain key_buf value from sgl.sg_iovs */

               memcpy( key_buf, ( char * )( ( sgl.sg_iovs )->iov_buf ) + offset, kds[ i ].kd_key_len );

               /* update offset for next key */
               offset += kds[ i ].kd_key_len;

               /* compute value for the key_buf */
               daos_size_t size = 0;
               size = val_size;
               daos_kv_get( oh, DAOS_TX_NONE, 0, key_buf, &size, rbuf, NULL );

            }
         }
      }

      free( ( char * )buf );
   }

   /* free resources */
   free( ( char * )key_buf );
   free( ( char * )val_buf );
   free( ( char * )rbuf );

   /* tear down */
   tear_down( );
}

// bnechmark function is getting called here.
static void kv_put_function( benchmark::State &state ) {
   /* perform setup */
   setup_main( );

   char key_name[ 20 ] = {
      0
   };

   unsigned int key_size = state.range( 0 );
   unsigned int val_size = state.range( 1 );
   unsigned int num_keys = state.range( 2 );

   /* allocate key and value buffers */
   char *key_buf = ( char * )calloc( key_size, sizeof( char ) ); // key buffer allocated
   char *val_buf = ( char * )calloc( val_size, sizeof( char ) ); // value buffer allocated
   memset( val_buf, 'z', val_size - 1 );                         // populate with some random value.

   /* actual computation starts here */
   for ( auto _ : state )
   {
      /* call daos_kv_put for state.range(2) times */
      for ( int i = 0; i < num_keys; i++ )
      {
         state.PauseTiming( );

         /* generate different key */
         memset( key_buf, 'x', key_size - 1 );
         sprintf( key_name, "%d", i );
         strncpy( ( char * )key_buf + strlen( key_buf ) - strlen( key_name ), ( char * )key_name, strlen( key_name ) );

         state.ResumeTiming( );

         /* actual function to mearsure time */
         daos_kv_put( oh, DAOS_TX_NONE, 0, ( char * )key_buf, key_size, val_buf, NULL );
      }
   }

   /* free resources */
   free( ( char * )key_buf );
   free( ( char * )val_buf );

   /* tear down */
   tear_down( );
}

// bnechmark function is getting called here.
static void kv_get_function( benchmark::State &state ) {
   /* perform setup */
   setup_main( );

   char key_name[ 20 ] = {
      0
   };

   unsigned int key_size = state.range( 0 );
   unsigned int val_size = state.range( 1 );
   unsigned int num_keys = state.range( 2 );

   /* allocate key and value buffers */
   char *key_buf = ( char * )calloc( key_size, sizeof( char ) ); // key buffer allocated
   char *val_buf = ( char * )calloc( val_size, sizeof( char ) ); // value buffer allocated

   memset( val_buf, 'z', val_size - 1 );

   char *rbuf = ( char * )calloc( val_size, sizeof( char ) ); // rbuf to check value

   if ( rbuf == NULL )
   {
      printf( "allocation failed \n" );

      return;
   }

   /* actual computation starts here */
   for ( auto _ : state )
   {
      /* call daos_kv_put for state.range(2) times */
      for ( int i = 0; i < num_keys; i++ )
      {
         state.PauseTiming( );

         /* generate different key */
         memset( key_buf, 'x', key_size - 1 );
         sprintf( key_name, "%d", i );
         strncpy( ( char * )key_buf + strlen( key_buf ) - strlen( key_name ), ( char * )key_name, strlen( key_name ) );

         daos_kv_put( oh, DAOS_TX_NONE, 0, ( char * )key_buf, val_size, val_buf, NULL );

         daos_size_t size = 0;
         size = val_size;

         state.ResumeTiming( );

         /* actual function to mearsure time */
         daos_kv_get( oh, DAOS_TX_NONE, 0, key_buf, &size, rbuf, NULL );
      }
   }

   /* free resources */
   free( ( char * )key_buf );
   free( ( char * )rbuf );
   free( ( char * )val_buf );

   /* tear down */
   tear_down( );
}

// Put keys
BENCHMARK( kv_put_function )
->ArgsProduct( { {
                  BM_KEY_64B, BM_KEY_128B, BM_KEY_256B, BM_KEY_512B, BM_KEY_1024B
               }, {
                     BM_VAL_1K, BM_VAL_4K, BM_VAL_8K, BM_VAL_16K, BM_VAL_32K
                  }, {
                     NR_KEYS_100, NR_KEYS_1000, NR_KEYS_10000, NR_KEYS_100000
                  }
               } )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

// Get keys
BENCHMARK( kv_get_function )
->ArgsProduct( { {
                  BM_KEY_64B, BM_KEY_128B, BM_KEY_256B, BM_KEY_512B, BM_KEY_1024B
               }, {
                     BM_VAL_1K, BM_VAL_4K, BM_VAL_8K, BM_VAL_16K, BM_VAL_32K
                  }, {
                     NR_KEYS_100, NR_KEYS_1000, NR_KEYS_10000, NR_KEYS_100000
                  }
               } )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

// list keys
BENCHMARK( kv_list_function )
->ArgsProduct( { {
                  BM_KEY_64B, BM_KEY_128B, BM_KEY_256B, BM_KEY_512B, BM_KEY_1024B
               }, {
                     BM_VAL_1K, BM_VAL_4K, BM_VAL_8K, BM_VAL_16K, BM_VAL_32K
                  }, {
                     NR_KEYS_100, NR_KEYS_1000, NR_KEYS_10000, NR_KEYS_100000
                  }, {
                     NR_QUERY
                  }
               } )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

// remove keys
BENCHMARK( kv_remove_function )
->ArgsProduct( { {
                  BM_KEY_64B, BM_KEY_128B, BM_KEY_256B, BM_KEY_512B, BM_KEY_1024B
               }, {
                     BM_VAL_1K, BM_VAL_4K, BM_VAL_8K, BM_VAL_16K, BM_VAL_32K
                  }, {
                     NR_KEYS_100, NR_KEYS_1000, NR_KEYS_10000, NR_KEYS_100000
                  }
               } )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

// Run the benchmark
BENCHMARK_MAIN( );
