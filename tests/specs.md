# kvlite

Key-value database wrapper for SQL database

## Collection

For creation or opening collection URI to backend is needed. Acceptable URIs for different backends described below.


### MySQL

```
mysql://username:password@hostname/database:collection
```

### Sqlite

```
sqlite://dbfile:collection
```

SQLite databases can be opened by using "sqlite" for the backend name (in the schema part of the URI). The hostname, username and password parts are ignored. In case when keyword `memory` is used for `dbfile`, kvlite will create an in-memory collection:
```
collection = kvlite.open('sqlite://memory:collection_name')
```
If `dbfile` is specified, it may be a relative path or an absolute path. Paths should be specified in the system dependent style. 
```
collection = kvlite.open('sqlite://testdb.sqlite:test_collection')
collection = kvlite.open('sqlite://home/projects/kvlite/testdb.sqlite:test_collection')
>>>
```
If the database file doesn't already exist, it will be created together with new collection. 


### PostgreSQL (not implemented yet)
```
postgres://username:password@hostname/database_name
```
