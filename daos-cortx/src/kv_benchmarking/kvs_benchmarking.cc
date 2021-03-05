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

#define KEY_SIZES 5
#define VAL_SIZES 5

#define ITERATION_CNT 100

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

   rc = uuid_parse( "11d1110f-f52e-43d2-8e11-7e0f2e8a6228", pool_uuid );

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

   unsigned int val_size = state.range( 0 );
   unsigned int key_size = state.range( 1 );
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
         sprintf( key_name, "key_%d", i );
         strncpy( ( char * )key_buf, ( char * )key_name, strlen( key_name ) );

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
static void kv_put_function( benchmark::State &state ) {
   /* perform setup */
   setup_main( );

   char key_name[ 20 ] = {
      0
   };

   unsigned int val_size = state.range( 0 );
   unsigned int key_size = state.range( 1 );
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

   state.counters[ "FooRate" ] = Counter( num_keys, benchmark::Counter::kIsRate );

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

   unsigned int val_size = state.range( 0 );
   unsigned int key_size = state.range( 1 );
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

// Put key
BENCHMARK( kv_put_function )
->ArgsProduct( { {
                  1 << 10, 4 << 10, 8 << 10, 16 << 10, 32 << 10 // value buffer sizes [1K, 4K, 8K, 16K, 32K]
               }, {
                     64, 128, 256, 512, 1024 // key sizes [64B, 128B, 256B, 512B, 1024B]
                  }, {
                     100 // number of keys generated for each value buffer size and key size combination
                  }
               } )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

// Get key
BENCHMARK( kv_get_function )
->ArgsProduct( { {
                  1 << 10, 4 << 10, 8 << 10, 16 << 10, 32 << 10
               }, {
                     64, 128, 256, 512, 1024
                  }, {
                     100
                  }
               } )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );

// Remove key
BENCHMARK( kv_remove_function )
->ArgsProduct( { {
                  1 << 10, 4 << 10, 8 << 10, 16 << 10, 32 << 10
               }, {
                     64, 128, 256, 512, 1024
                  }, {
                     100
                  }
               } )
->Iterations( 1 )
->Unit( benchmark::kMillisecond );
// Run the benchmark
BENCHMARK_MAIN( );
