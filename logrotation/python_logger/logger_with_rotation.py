#! /usr/bin/python3

from cortx.utils.log import Log
import time

Log.init('logger_with_rotation',
         '/var/log/component/',
         backup_count=5,
         file_size_in_mb=0.1)

i = 0
try:
    while True:
        Log.info(f"Logging the pizza count : {i} 🍕")
        i += 1
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting the python logger. Byee !! 🙋")
    exit(0)
except Exception as e:
    print(e)
    exit(1)
