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
query_body = {
  "query": {
      "match": {
          "some_field": "search_for_this"
      }
  }
}
```
You can pass the dictionary data for the query directly to the search method at the time of the call.

The only two required parameters for the Search API in Python are the index you want to search, and the body of the Elasticsearch query:

```python
elastic_client.search(index="some_index", body=some_query)
```

 
 

 
