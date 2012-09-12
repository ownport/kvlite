# kvlite

kvlite is small library for storing documents in SQL databases. At the moment supported MySQL and SQLite. A document can be string, list/tuple or dictionary. But of course it possible to define own serialization to store data in kvlite database.

A collection is a group of documents stored in kvlite, and it can be thought of as roughly the equivalent of a  table in a relational database.

## Collection Utils

 - open(uri)        - open collection
 - remove(uri)      - remove collection
 - get_uuid(amount) - get list of uuid 
 
To get started just open() function is needed.

URI format is:

 - for mysql: `mysql://username:password@hostname:port/database.collection_name`
 - for sqlite: `sqlite://path-to-sqlite-file:collection_name` or `sqlite://memory:collection_name`
 
In case when sqlite is in use two variants of collection is possible: in file and in memory.

The function open(uri) returns MysqlCollection or SqliteCollection object

## Collection

MysqlCollection and SqliteCollection have the same methods:

 - get_uuid()   - in case of mysql use, this function will be working faster than for sqlite
 - get(k)       - if k(key) is not defined, the function get() returns the list of all documents in collection. Otherwise key/value pair is returned for defined k(key)
 - put(k,v)     - put key/value to storage. The key has limitation - only 40 bytes length. The value can be string, list or tuple, dictionary
 - delete(k)    - delete key/value pair
 - keys()       - returns the list of all keys in collection
 - count()      - returns the amount of documents in collection
 - commit()     - as kvlite based on transactional databases, commit() is used for commitment changes in collection
 - close()      - close connection to database

## CollectionManager

Sometimes it will needed to manage collections: create, check if exists, remove. For these operations you can use CollectionManager. This class has the next methods:

 - parse_uri(uri)   - depends on type of database, the function parse_uri() can returns deferent result based on which backend is used
 - create(name)     - create collection
 - connection       - returns refernce to database collection
 - collection_class - returns class MysqlCollection or SqliteCollection depend on backend parameter in URI
 - collections()    - returns the list of collections in database
 - remove(name)     - remove collection
 - close()          - close connection to database

### Links
 * [What are the performance characteristics of sqlite with very large database files?](http://stackoverflow.com/questions/784173/what-are-the-performance-characteristics-of-sqlite-with-very-large-database-file)
 * [Best practice: Optimizing SQLite database performance](http://docs.blackberry.com/en/developers/deliverables/17952/BP_Optimizing_SQLite_database_performance_1554266_11.jsp)
 * [Limits In SQLite](http://www.sqlite.org/limits.html)
 * [U1DB](http://packages.python.org/u1db/) is a database API for synchronised databases of JSON documents. It’s simple to use in applications, and allows apps to store documents and synchronise them between machines and devices. U1DB itself is not a database: instead, it’s an API which can be backed by any database for storage. This means that you can use u1db on different platforms, from different languages, and backed on to different databases, and sync between all of them.
 * [kvlite project on Goolge Code](http://code.google.com/p/kvlite/)
 * [Storm](https://storm.canonical.com/) is an object-relational mapper (ORM) for Python developed at Canonical.
