#!/bin/bash

# add config like this in your agent conf.json{or configuration} file
#{
# "type": "keyprefix",
# "prefix": "foo/",
# "args": ["/usr/bin/consulWatcherHander.sh", "Yourname"]
#}

# example of using arguments to a script
echo "My first name is $1" >> path_to_this_file.txt
now=$(date +"%T")
echo "Current time : $now" >> path_to_this_file.txt
