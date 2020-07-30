 # How to retrieve data from elasticsearch.
 
There are three different ways to scroll Elasticsearch documents using the Python client library using: 
   1. The client’s search() method
   2. The helpers library’s scan() method
   3. The client’s scroll() method.
 ## The client’s search() method
 Allows you to execute a search query and get back search hits that match the query.Several options for this API can be specified using a query parameter or a request body    parameter. If both parameters are specified, only the query parameter is used.The first step is to create a JSON object (using a dict object in Python) with the search size and query Elasticsearch fields for the dictionary keys.*By default search() returns 10 records.* Use size parameter to specify no of documents client want to retrieve.
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
This is a basic way to call search. The search request body may contain many [parameters.](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-scroll)
#### Note: 
- *Result of search() depends on size parameter(by default 10 records)*
- *Use of only search() may lead to loss of some desired records, If client demanding more records than limit of search().*
- *Response of search() includes json object along with scroll-id.*
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

#### Note:
- *Scan will retrieve all records from elasticsearch at a time.*
- *Response of scan() should return a generator object. It may or may not include scroll_id(depend on version of elasticsearch).*
- *Scan() is Simple abstraction on top of the scroll() api and a simple iterator that yields all hits as returned by underlining scroll requests. *Scan and scroll method is replaced by scan and search for newer version of elasticsearch.*


## The client’s scroll() method.
*Scrolling in Elasticsearch allows you retrieve a large number of documents, in steps or iterations, similar to pagination or a “cursor” in relational databases.*
you can also use the client’s low-level scroll() method designed to work with Elastic’s Scroll API.
### Scroll
While a search request returns a single “page” of results, the scroll API can be used to retrieve large numbers of results (or even all results) from a single search request, in much the same way as you would use a cursor on a traditional database.

Scrolling is not intended for real time user requests, but rather for processing large amounts of data, e.g. in order to reindex the contents of one index into a new index with a different configuration.

The results that are returned from a scroll request reflect the state of the index at the time that the initial search request was made, like a snapshot in time. Subsequent changes to documents (index, update or delete) will only affect later search requests.
### Scroll()
In order to use scrolling, the initial search request should specify the scroll parameter in the query string, which tells Elasticsearch how long it should keep the “search context” alive eg ?scroll=1m.
```python
# declare a filter query dict object
match_all = {
    "size": 50,
    "query": {
        "match_all": {} 
        # add any filter 
    }
}
# make a search() request to get all docs in the index
res = client.search(
    index="helper",
    body=match_all,
    scroll='2m'
)
```
- The result from the above request includes a _scroll_id, which should be passed to the scroll API in order to retrieve the next batch of results.
- The scroll parameter tells Elasticsearch to keep the search context open for another 1m
- The initial search request and each subsequent scroll request each return a _scroll_id. While the _scroll_id may change between requests, it doesn’t always change — in any   case, only the most recently received _scroll_id should be used.
- If the request specifies aggregations, only the initial search response will contain the aggregations results.
- Scroll requests have optimizations that make them faster when the sort order is _doc. If you want to iterate over all documents regardless of the order, this is the most efficient option:

```python
client.scroll(scroll_id = sid, scroll = '2m')
```
A scroll returns all the documents which matched the search at the time of the initial search request. It ignores any subsequent changes to these documents. The scroll_id identifies a search context which keeps track of everything that Elasticsearch needs to return the correct documents. The search context is created by the initial request and kept alive by subsequent requests.

The scroll parameter (passed to the search request and to every scroll request) tells Elasticsearch how long it should keep the search context alive. Its value (e.g. 1m) does not need to be long enough to process all data — it just needs to be long enough to process the previous batch of results. Each scroll request (with the scroll parameter) sets a new expiry time. If a scroll request doesn’t pass in the scroll parameter, then the search context will be freed as part of that scroll request.

### Issues caused by having too many scrolls open

To prevent against issues caused by having too many scrolls open, the user is not allowed to open scrolls past a certain limit. By default, the maximum number of open scrolls is 500. This limit can be updated with the search.max_open_scroll_context cluster setting.

### Clear-scroll API:

Search context are automatically removed when the scroll timeout has been exceeded. However keeping scrolls open has a cost, as discussed so scrolls should be explicitly cleared as soon as the scroll is not being used anymore using the clear-scroll API



















 
 

 
