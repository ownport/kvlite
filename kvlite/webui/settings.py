#
#   Settings
#
import os
import kvlite

# During early development, the debug mode can be very helpful.
# In this mode, Bottle is much more verbose and provides helpful 
# debugging information whenever an error occurs. It also 
# disables some optimisations that might get in your way and adds 
# some checks that warn you about possible misconfiguration.
# Here is an incomplete list of things that change in debug mode:
#
# - The default error page shows a traceback.
# - Templates are not cached.
# - Plugins are applied immediately.
#

# Web UI host
WEBUI_HOST = '127.0.0.1'

# Web UI port
WEBUI_PORT = 8080

# Just make sure not to use the debug mode on a production server.
DEBUG_MODE = True

# The absolute path to the directory where static files are located
STATIC_PATH = os.path.join(
    os.path.dirname(os.path.abspath(kvlite.__file__)), 
    'webui/static'
)

# The absolute path to the logfile
WEBUI_LOGFILE = os.path.join(os.getcwd(), 'log/kvlite-webui.log')

# The absolute path to the pidfile. It's required when kvlite-webui is running as service
WEBUI_PIDFILE = os.path.join(os.getcwd(), 'run/kvlite-webui.pid')

