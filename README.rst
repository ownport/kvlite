======
kvlite
======

kvlite is small open-source library for storing documents in SQL databases. Only three methods are needed to manipulate documents in database: get(), put(), delete(). At the moment supported MySQL and SQLite databases only. A document can be string, list/tuple or dictionary. Default serialization is based on cPickleSerializer methods but of course it is possible to define own serialization to store data in kvlite databases. 

A ``document`` is a string, list/tuple, dictionary or any structure which can be serialized by cPickle, JSON or own serializer.

A ``collection`` is a group of documents stored in kvlite. It can be thought of as roughly the equivalent of a table in a relational database.

The format of ``uri`` (uniform resource identifier) for databases:

 * for mysql: 'mysql://username:password@hostname:port/database.collection_name'
 * for sqlite: 'sqlite://path-to-sqlite-file:collection_name' or 'sqlite://memory:collection_name'
 
In case when sqlite is in use two variants of collection is possible: store data in file or store data in memory.


Installation
============

please check installation guideline <https://github.com/ownport/kvlite/blob/master/docs/install.md>

Usage
=====
 - Examples <https://github.com/ownport/kvlite/blob/master/docs/examples.md> 
 - Search criterias <https://github.com/ownport/kvlite/blob/master/docs/search-criterias.md>

Developer interface
===================
 - Utils <https://github.com/ownport/kvlite/blob/master/docs/api.md#collection-utils>
 - Collection <https://github.com/ownport/kvlite/blob/master/docs/api.md#collection>
 - CollectionManager <https://github.com/ownport/kvlite/blob/master/docs/api.md#collectionmanager>
 - Serializers <https://github.com/ownport/kvlite/blob/master/docs/api.md#serializers>
 - kvlite diagram <https://raw.github.com/ownport/kvlite/master/docs/kvlite.png>

Articles
========
 - How FriendFeed uses MySQL to store schema-less data <https://github.com/ownport/kvlite/blob/master/docs/articles/friendfeed-mysql-datastore.md>
 
Links
=====
 - Links <https://github.com/ownport/kvlite/blob/master/docs/links.md> 


