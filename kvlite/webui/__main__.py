import os
import bottle

from kvlite.webui import settings

# favicon.ico handling
def handle_favicon():
    return bottle.static_file('images/favicon.ico', root=settings.STATIC_PATH)

# static files handling
def handle_static(filepath):
    return bottle.static_file(filepath, root=settings.STATIC_PATH)

    
@bottle.route('/')
def index():
    return bottle.static_file('index.html', root='static/html/')

@bottle.route('/static/<filename>')
def static_files(filename):
    ''' handle static files
    '''
    return bottle.static_file(filename, root='static/')

if __name__ == '__main__':
    
    bottle.run(
                host=settings.WEBUI_HOST, 
                port=settings.WEBUI_PORT, 
                debug=settings.DEBUG_MODE
    )
    
