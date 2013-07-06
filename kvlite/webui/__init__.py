import os

from bottle import run
from bottle import route
from bottle import static_file

@route('/')
def index():
    return static_file('index.html', root='static/html/')

@route('/static/<filename>')
def static_files(filename):
    ''' handle static files
    '''
    return static_file(filename, root='static/')

run(host='localhost', port=8080, debug=True)
