import os
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

@bottle.route('/collection/<name>/item/<item_key>', method="GET")
@bottle.route('/collection/<name>/item/<item_key>', method="POST")
def get_item(name, item_key):
    ''' return item data 
    '''
    try:
        collection_uri = settings.COLLECTIONS[name]
        collection = kvlite.open(collection_uri)
    except KeyError:
        return {'error': 'The collection %s is not found' % name, 'status': 'NOT OK'}

    item_value = bottle.request.POST.get('value', '')     
    if item_value:
        print 'key: ' + item_key
        print 'value: ' + item_value 
        return {
                    'status': 'OK', 
        }
    else:        
        item_key, item_value = collection.get({'_key': item_key})
        collection.close()
        return {
                    'status': 'OK', 
                    'item': {'key': item_key, 'value': item_value},
        }

if __name__ == '__main__':
    
    bottle.run(
                host=settings.WEBUI_HOST, 
                port=settings.WEBUI_PORT, 
                debug=settings.DEBUG_MODE
    )
    
