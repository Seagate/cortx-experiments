 # How to retrieve data from elasticsearch.
 
There are three different ways to scroll Elasticsearch documents using the Python client library using: 
   1. The client’s search() method
   2. The helpers library’s scan() method
   3. The client’s scroll() method.
 ## The client’s search() method
 Allows you to execute a search query and get back search hits that match the query.Several options for this API can be specified using a query parameter or a request body    parameter. If both parameters are specified, only the query parameter is used.The first step is to create a JSON object (using a dict object in Python) with the search size and query Elasticsearch fields for the dictionary keys.*By default search() returns 10 records.* Use size parameter to specify no of documents.
 We’ll need to create a Python dictionary that will be passed to the client’s search() method. This dictionary will contain key-value pairs that represent the search parameters, the fields to be searched and the values.

The dictionary will be passed to the body parameter of the method. The first key should be the Elasticsearch "query" field.Here’s what a basic search query would look like in a Python script:


```python
any_query = {
  "query": {
      "size": No_of_records,
      "match": {
          "some_field": "search_for_this"
      }
  }
}
```
You can pass the dictionary data for the query directly to the search method at the time of the call.

The only two required parameters for the Search API in Python are the index you want to search, and the body of the Elasticsearch query:

```python
elastic_client.search(index="some_index", body=any_query)
```
## The helpers library’s scan() method

scan() method is a part of the client’s helpers library, and it’s basically a wrapper for the aforementioned scroll() method. The **key difference** us that helpers.scan() will return a generator instead of a JSON dictionary response. 
```python
elasticsearch.helpers.scan(client, query=None, scroll='5m', raise_on_error=True, preserve_order=False, size=1000, request_timeout=None, clear_scroll=True, scroll_kwargs=None, **kwargs)
```

By default scan does not return results in any pre-determined order. To have a standard order in the returned documents (either by score or explicit sort definition) when scrolling, use preserve_order=True. This may be an expensive operation and will negate the performance benefits of using scan.

Parameters:	
1. client – instance of Elasticsearch to use
2. query – body for the search() api
3. scroll – Specify how long a consistent view of the index should be maintained for scrolled search.**Not supported in elasticsearch 7.8.X**
4. raise_on_error – raises an exception (ScanError) if an error is encountered (some shards fail to execute). By default we raise.
5. preserve_order – don’t set the search_type to scan - this will cause the scroll to paginate with preserving the order. Note that this can be an extremely expensive operation    and can easily lead to unpredictable results, use with caution.
6. size – **size (per shard) of the batch send at each iteration.**  *Note:size is not no of records*
7. request_timeout – explicit timeout for each call to scan
8. clear_scroll – explicitly calls delete on the scroll id via the clear scroll API at the end of the method on completion or error, defaults to true.
9. scroll_kwargs – additional kwargs to be passed to scroll()

*Note:Scan will retrieve all records from elasticsearch at a time.*





 
 

 
