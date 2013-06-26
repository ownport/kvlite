# Examples

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

