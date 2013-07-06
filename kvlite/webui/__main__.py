import os
import bottle

from kvlite.webui import settings

@bottle.route('/')
def index():
    ''' handle index.html
    '''
    return bottle.static_file('html/index.html', root=settings.STATIC_PATH)

@bottle.route('/favicon.ico')
def index():
    ''' handle favicon.ico
    '''
    return bottle.static_file('img/favicon.ico', root=settings.STATIC_PATH)

@bottle.route('/img/<filename>')
def static_img_files(filename):
    ''' handle image files
    '''
    return bottle.static_file(filename, root=os.path.join(settings.STATIC_PATH, 'img'))

@bottle.route('/css/<filename>')
def static_css_files(filename):
    ''' handle css files
    '''
    return bottle.static_file(filename, root=os.path.join(settings.STATIC_PATH, 'css'))

@bottle.route('/js/<filename>')
def static_js_files(filename):
    ''' handle JavaScript files
    '''
    return bottle.static_file(filename, root=os.path.join(settings.STATIC_PATH, 'js'))

if __name__ == '__main__':
    
    bottle.run(
                host=settings.WEBUI_HOST, 
                port=settings.WEBUI_PORT, 
                debug=settings.DEBUG_MODE
    )
    
