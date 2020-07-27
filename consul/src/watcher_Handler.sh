#!/bin/bash

# example of using arguments to a script
echo "My first name is $1" >> /root/rajkumar/fuzzyfile.txt
now=$(date +"%T")
echo "Current time : $now" >> /root/rajkumar/fuzzyfile.txt
