# kvlite

kvlite is small library for storing documents in SQL databases. At the moment supported MySQL and SQLite. A document can be string, list/tuple or dictionary. But of course it possible to define own serialization to store data in kvlite database.

A collection is a group of documents stored in kvlite,  and can be thought of as roughly the equivalent of a  table in a relational database.

## Collection Utils

 - open(uri)
 - remove(uri)

## Collection

## MySQL Collection

## SQLite Collection


### Links
 * [What are the performance characteristics of sqlite with very large database files?](http://stackoverflow.com/questions/784173/what-are-the-performance-characteristics-of-sqlite-with-very-large-database-file)
 * [Best practice: Optimizing SQLite database performance](http://docs.blackberry.com/en/developers/deliverables/17952/BP_Optimizing_SQLite_database_performance_1554266_11.jsp)
 * [Limits In SQLite](http://www.sqlite.org/limits.html)
 * [U1DB](http://packages.python.org/u1db/) is a database API for synchronised databases of JSON documents. It’s simple to use in applications, and allows apps to store documents and synchronise them between machines and devices. U1DB itself is not a database: instead, it’s an API which can be backed by any database for storage. This means that you can use u1db on different platforms, from different languages, and backed on to different databases, and sync between all of them.
 * [kvlite project on Goolge Code](http://code.google.com/p/kvlite/)
 * [Storm](https://storm.canonical.com/) is an object-relational mapper (ORM) for Python developed at Canonical.
