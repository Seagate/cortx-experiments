#!/usr/bin/env bash
#set -x

# Reads in SQL outputed records representing s3 requests
# Calculate time for each S3 request.

if [[ $# -ne 1 ]]
then
  echo -e "Please provide SQL log file\n"
  exit 1;
fi

cnt=0
SQL_FILE=$1
SQL_FILE_OUT=$SQL_FILE.out
truncate -s 0 $SQL_FILE_OUT
while read line
  do
    var_start_line=$line
    if [[ "$var_start_line" =~ "|START" ]]
    then
      # var_start_line contains START state 
      start_time=$(echo $var_start_line | cut -d "|" -f 1)
      action_text=$(echo $var_start_line | cut -d "|" -f 5)
    else
      if [[ "$var_start_line" =~ "|COMPLETE" ]]
      then
        #Append final part of Action text
        action_text+="\n"$(echo $var_start_line | cut -d "|" -f 5)
	
        if [[ "$action_text" =~ "S3GetObjectAction" ]]
	then
          #This is S3 Get Object request
          ((cnt+=1))
          end_time=$(echo $var_start_line | cut -d "|" -f 1)
          time_in_nano=$((end_time-start_time))
          time_in_milli=$(echo "scale = 2; $time_in_nano / 1000000" | bc)
          time_dummy=$(($time_in_nano / 1000000))
          #echo -e "Time in milli:${time_in_milli}\n"
          LINE=$(echo "$var_start_line" | sed -E 's/(.*)(\|COMPLETE)/\1/')
          if [ 1 -eq `echo "$time_in_milli < 1" | bc` ]
          then
            time_in_milli="0$time_in_milli"
            #echo -e "$time_in_milli\n"
          fi
          echo -e "$LINE|$time_in_milli" >> $SQL_FILE_OUT
	  #echo -e "\nAction text:\n"$action_text
	fi
      else
        #Append Action text
        action_text+="\n"$(echo $var_start_line | cut -d "|" -f 5)
      fi
    fi
  done < $SQL_FILE
 echo -e "\nTotal S3 Get requests scanned: $cnt"

