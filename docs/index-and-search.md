# Index and search in kvlite

New in version 0.4.6

ideas was taken from [MongoDB Indexing Overview](http://docs.mongodb.org/manual/core/indexes/)

To make indexing and searching data in kvlite database were added three functions: make_index(), remove_index() and search(). Indexes often allow to increase the performance of queries. However, each index creates a slight overhead for every write operation. 

- kvlite defines indexes on a per-collection level.
- index can be created in different database with different database engine
- every search query uses only one index
- you can create indexes on any field within any document or sub-document.
- you can create indexes on a single field or on multiple fields using a compound index.
- you can create compound indexes with multiple fields, so that a single query can match multiple components using the index without needing to scan (as many) actual documents.

## index

def make_index(source_uri, parameters, index_uri)

- source_uri
- parameters
- index_uri

The examples of index definitions:

```
{ "field": 1 }
{ "field0.field1": 1 }
{ "field0": 1, "field1": 1 }
```

For each field in the index you will specify either 1 for an ascending order or -1 for a descending order, which represents the order of the keys in the index.

You can create indexes on fields that exist in sub-documents within your collection.

```
{
    'b'
}
```



def remove_index(index_uri)

### Index Limitations

There's no limitation in creation indexes.

## search 

def search(index_uri, search_criteria)

- index_uri
- search_criteria


