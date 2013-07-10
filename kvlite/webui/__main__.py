import os
import bottle
import kvlite

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
    return {'collections': settings.COLLECTIONS.keys() }

@bottle.route('/collection/<name>/')
def get(name):
    ''' return collection data 
    '''
    try:
        collection_uri = settings.COLLECTIONS[name]
    except KeyError:
        return {'error': 'The collection %s is not found' % name, 'status': 'NOT OK'}
    collection = kvlite.open(collection_uri)
    return {'error': '', 'status': 'OK', 'data': [kv for kv in collection.get()]}

if __name__ == '__main__':
    
    bottle.run(
                host=settings.WEBUI_HOST, 
                port=settings.WEBUI_PORT, 
                debug=settings.DEBUG_MODE
    )
    
