import os
import json
import bottle
import kvlite

from math import ceil
from kvlite.webui import settings


#
#   Service commands
#
@bottle.route('/')
def index():
    ''' handle index.html
    '''
    return bottle.static_file('html/index.html', root=settings.STATIC_PATH)

@bottle.route('/favicon.ico')
def get_favicon():
    ''' handle favicon.ico
    '''
    return bottle.static_file('img/favicon.ico', root=settings.STATIC_PATH)

@bottle.route('/img/<filename>')
def get_static_img_files(filename):
    ''' handle image files
    '''
    return bottle.static_file(filename, root=os.path.join(settings.STATIC_PATH, 'img'))

@bottle.route('/css/<filename>')
def get_static_css_files(filename):
    ''' handle css files
    '''
    return bottle.static_file(filename, root=os.path.join(settings.STATIC_PATH, 'css'))

@bottle.route('/js/<filename>')
def get_static_js_files(filename):
    ''' handle JavaScript files
    '''
    return bottle.static_file(filename, root=os.path.join(settings.STATIC_PATH, 'js'))

#
#   kvlite's webui api
#
@bottle.route('/collections')
def collections_list():
    ''' returns the list of collections
    '''
    return {
                'status': 'OK',
                'collections': settings.COLLECTIONS.keys() }

@bottle.route('/key')
def get_key():
    ''' return generated key 
    '''
    import hashlib
    import datetime
    
    str_now = str(datetime.datetime.now())
    key = hashlib.sha1(str_now).hexdigest()
    return { 'status': 'OK',  'key': key, }

@bottle.route('/collection/<name>/page/<page>')
def get_page(name, page):
    ''' return collection data for specific page
    '''
    page = int(page)
    try:
        collection_uri = settings.COLLECTIONS[name]
    except KeyError:
        return {'error': 'The collection %s is not found' % name, 'status': 'NOT OK'}
    collection = kvlite.open(collection_uri)
    last_page = collection.count / settings.ITEMS_PER_PAGE
    #last_page = int(ceil(collection.count / float(settings.ITEMS_PER_PAGE)))
    data = [kv for kv in collection.get(offset=page * settings.ITEMS_PER_PAGE, limit=settings.ITEMS_PER_PAGE)]
    collection.close()
    return {
                'status': 'OK', 
                'last_page': last_page,
                'data': data,
    }

def create_update_item(collection, k, v):
    ''' create or update item
    '''
    try:
        collection_uri = settings.COLLECTIONS[collection]
        collection = kvlite.open(collection_uri)
    except KeyError:
        return {'error': 'The collection %s is not found' % name, 'status': 'NOT OK'}

    if v:
        try:
            collection.put(k, json.loads(v))
            collection.commit()
            collection.close()
            return { 'status': 'OK', }
        except Exception, err:
            return {
                'status': 'Error',
                'message': err, 
            }

def get_item(collection, k):
    ''' get item details   
    '''
    try:
        collection_uri = settings.COLLECTIONS[collection]
        collection = kvlite.open(collection_uri)
    except KeyError:
        return {'error': 'The collection %s is not found' % name, 'status': 'NOT OK'}
    
    k, v = collection.get({'_key': k})
    collection.close()
    return { 'status': 'OK', 'item': {'key': k, 'value': v}, }
    
def delete_item(collection, k):
    ''' delete item by key
    '''
    try:
        collection_uri = settings.COLLECTIONS[collection]
        collection = kvlite.open(collection_uri)
    except KeyError:
        return {'error': 'The collection %s is not found' % name, 'status': 'NOT OK'}

    try:
        collection.delete(k)
        collection.commit()
        collection.close()
        return { 'status': 'OK', }
    except:
        return { 'status': 'Error', 'message': 'Cannot delete the item by key', }
    

@bottle.route('/collection/<collection_name>/item/<item_key>', method="GET")
@bottle.route('/collection/<collection_name>/item/<item_key>', method="POST")
@bottle.route('/collection/<collection_name>/item/<item_key>', method="DELETE")
def handle_item(collection_name, item_key):
    ''' handle item and return result 
    '''
    if bottle.request.method == 'GET':    
        return get_item(collection_name, item_key)

    elif bottle.request.method == 'POST':
        return create_update_item(collection_name, item_key, bottle.request.POST.get('value', ''))
        
    elif bottle.request.method == 'DELETE':    
        return delete_item(collection_name, item_key)        
    
    else:        
        return { 'status': 'Error', 'message': 'Unknown method %s' % bottle.request.method, }

if __name__ == '__main__':
    
    bottle.run(
                host=settings.WEBUI_HOST, 
                port=settings.WEBUI_PORT, 
                debug=settings.DEBUG_MODE
    )
    
