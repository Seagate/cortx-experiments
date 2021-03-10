# Python program to convert
# JSON file to CSV
#
# USAGE : 1. Create json file with report : 
#            $ ./mybenchmark_out --benchmark_out=data.json
#         2. run script :
#            $ python3 json_report_to_csv.py    

import json
import csv
import pandas as pd

# opening JSON report and loading the data
# into the variable data
with open('data.json') as json_file:
    data = json.load(json_file)

# choose benchmarks report key
bm_data = data['benchmarks']

# choose one test at a time to alter fields 
for element in bm_data:
    # remove unwanted fields
    element.pop('run_type', None)
    element.pop('run_name', None)
    element.pop('repetitions', None)
    element.pop('repetition_index', None)

    # rename fields for more readability
    element['realtime_ms'] = element.pop('real_time', None)
    element['cputime_ms'] = element.pop('cpu_time', None)

    # extract numbers from the test name
    list_num = []
    for s in element['name'].split('/'):
        if s.isdigit():
            list_num.append(s)
            
    # get key-size, value-size and number of operations
    str1 = str(list_num[0])
    str2 = str(list_num[1])
    str3 = str(list_num[2])

    # create new fields - keysize_valsize and nr_ops
    element['keysize_valsize']= str1 + str2
    element['nr_ops']= str3
    
    # create more fields using existing data points
    element['realtime_per_op_ms']=float(element['realtime_ms'])/int(element['nr_ops'])
    element['cputime_per_op_ms']=float(element['cputime_ms'])/int(element['nr_ops'])

# open new file to store updated fields
with open('fine_data.json', 'w') as data_file:
    data = json.dump(data, data_file)

# close file
data_file.close()

# now we will open a file for writing
data_file = open('benchmark_data_file.csv', 'w')

# create the csv writer object
csv_writer = csv.writer(data_file)

# Counter variable used for writing
# headers to the CSV file
count = 0

for bm in bm_data:
    if count == 0:

        # Writing headers of CSV file
        header = bm.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(bm.values())

# close file
data_file.close()

# reorder columns in csv file using pandas library
df = pd.read_csv("benchmark_data_file.csv")
df = df[["name", "keysize_valsize", "nr_ops", "realtime_ms", "cputime_ms", "realtime_per_op_ms", "cputime_per_op_ms","iterations", "threads"]]
df.head()
print (df)

# dump updated dataframe(df) to csv file
df.to_csv("benchmark_data_file.csv", index=False)
