# Examples

## kvlite.cli

`kvlite.cli` module is used for get access to kvlite databases via console

```
$ python -m kvlite.cli
kvlite>
kvlite> ?

   help <command>	show <command> help
   version		show kvlite version
   licence		show licence
   history		show commands history 
   exit			exit from console 

   create <name> <uri>		    create new collection (if not exists)
   use <collection_name>	    use the collection as the default (current) collection
   show collections <details>	list of available collections
   remove <collection_name>	    remove collection
   import <filename>		    import collection configuration from JSON file
   export <filename>		    export collection configurations to JSON file
   copy <source> <target>	    copy data from source kvlite database to target kvlite database
                                <source> - reference name to source database
                                <target> - reference name to target database
                                for creating reference name, use `create` command

   hash [string]	    generate sha1 hash, random if string is not defined
   items		        list of collection's items 
   get <key>		    show collection entry by key
   put <key> <value>	store entry to collection, where <value> is data in JSON format
   delete <key>		    delete entry by key 
   count		        show the amount of entries in collection 
   scheme		        show structure of collection
   index <details>	    make index for current collection

kvlite> 
```

## Bulk put()

When you need to insert many documents to kvlite database

```python
import kvlite
collection = kvlite.open('sqlite://memory:test')
kvs = [(k,'value:%d' % k) for k in xrange(100)]
collection.put(kvs)
collection.commit()
```

## Pagination

To be described later

## Migration data

### Copy data from database (v0.4.5) to database (v0.5.1)

Most simple way to migrate data from v0.4.5 database to v0.5.1 database is copy data

```python
>>> import kvlite
>>> source = kvlite.open('sqlite://tests/db/test1.kvlite', cPickleSerializer)
>>> target = kvlite.open('sqlite://tests/db/test2.kvlite', cPickleSerializer)
>>> kvlite.copy(source, target)
>>>
```

