# Search criterias

The simplest way to find document byt its key

```python
>>> collection.get({'_key': 'c3c28de8ea56ec4210d6939596c8a0c907c69e39'})
(
  'c3c28de8ea56ec4210d6939596c8a0c907c69e39', 
  {
    'title': 'Blog post 1',
    'description': 'Just sample post 1',
    'datetime': '2012-11-03T12:00:00',
    'keywords': ['post', 'blog', 'example', 'kvlite'], 
  })
```

If known more document's keys, it's possible to add it to get() as 
list of parameters

```python
>>> collection.get({
... '_key': [
... 'c3c28de8ea56ec4210d6939596c8a0c907c69e39',
... '8d633daeab8f4740b34bfc9b700a6cd328ceb96a',
... 'ffc40a18975468fdc2f74cb4314379d2ed8c8d99']})

((
  'c3c28de8ea56ec4210d6939596c8a0c907c69e39', 
  {
    'title': 'Blog post 1',
    'description': 'Just sample port 1',
    'datetime': '2012-11-03T12:00:00',
    'keywords': ['port', 'blog', 'example', 'kvlite'], 
  }
),
(
  '8d633daeab8f4740b34bfc9b700a6cd328ceb96a', 
  {
    'title': 'Blog post 2',
    'description': 'Just sample port 2',
    'datetime': '2012-11-03T12:00:00',
    'keywords': ['port', 'blog', 'example', 'kvlite'], 
  }
),
(
  'ffc40a18975468fdc2f74cb4314379d2ed8c8d99', 
  {
    'title': 'Blog post 3',
    'description': 'Just sample port 3',
    'datetime': '2012-11-03T12:00:00',
    'keywords': ['port', 'blog', 'example', 'kvlite'], 
  }
),)
  
```



 
