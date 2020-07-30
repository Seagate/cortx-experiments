# Code is divided into two parts.Search api provides result for first batch
# While loop will fetch remaining batches
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time
import json
elastic_client = Elasticsearch('localhost:9200')
# declare a filter query
filter = {
    "size": 50,
    "query":{
        "bool":{
            "must_not":{
                "match":{
                    "site_id" : "PUNE"
                }
            },
            "should":{
                "match":{
                    'alert_type': 'High'
                }
            }
        }


    }
}
# make a search() request to get all docs in the index
res = elastic_client.search(
    index="test_index",
    body=filter,
    scroll='2m'

)
# Print records of first batch
print ("total hits:", len(res["hits"]["hits"]))
# Get scroll id for scroll api
sid = res['_scroll_id']
scroll_size = len(res['hits']['total'])
all_hits = res['hits']['hits']
for num, doc in enumerate(all_hits):
    print ("DOC ID:", doc["_id"])
    for key, value in doc.items():
        print (key, "-->", value)
    print ("\n\n")

while (scroll_size > 0):
    print("Scrolling...")
    res = elastic_client.scroll(scroll_id = sid, scroll = '2m')
    # Update the scroll ID
    sid = res['_scroll_id']
    # Get the number of results that we returned in the last scroll
    scroll_size = len(res['hits']['hits'])
    all_hits = res['hits']['hits']
    for num, doc in enumerate(all_hits):
        print("DOC ID:", doc["_id"])
        for key, value in doc.items():
            print(key, "-->", value)
        print("\n\n")
    print("scroll size: " + str(scroll_size))
    # Clear memory for this batch
    elastic_client.clear_scroll(body={'scroll_id': [sid]})



