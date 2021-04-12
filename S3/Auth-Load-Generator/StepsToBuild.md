BUILD:
======
-Correct way:
1) Follow the steps on https://github.com/rhymu8354/Aws to checkout and build.
2) Replace SignApi.cpp in the library with the one from TestCode folder and build the library.
2) Yum install Curl and gFlag libraries
3) Compile and Link pthread_client with the libraries

Else

-Working-TestCode:
This is a messy way to build, but it works :)
At some point, only the files needed for binary should be linked
and the build steps should be moved to a Makefile.Till then,
1)Untar Working-Testcode and cd into it.
2)Compile *all* the .c in the folder.
   g++ -c --std=c++11 httprequest.cpp
3)Link the object files
   g++ -lgflags -lcurl -ggdb -g MessageHeaders.o pthread_client.o StringExtensions.o SignApi.o Uri.o CharacterSet.o PercentEncodedCharacterDecoder.o Sha2.o Hmac.o Request.o Server.o Deflate.o Scheduler.o DiagnosticsSender.o Response.o -pthread -o pthread_client

EXECUTE:
========
./pthread_client -port 9080 127.0.0.1 4000 1
replace 
9080 with Port Number
127.0.0.1 with IP address of the server
4000 with Num of threads to spawn
1 This is ToDo.The code needs to be modified to take in secret key instead, but for now give 1
