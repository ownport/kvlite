# Installation

To install kvlite you just need to copy two files: kvlite.py and kvlite-cli.py. Second one is optional and it's needed only if you need to have access to kvlite collections via console. Feel free to use kvlite-cli.py as example how to work with kvlite library.

If `pip <http://www.pip-installer.org/>` installed in your system, you can install kvlite via

    pip install kvlite
    
For mysql support `mysql-python` package is required

    pip install mysql-python
    
Note! If during installation mysql-python will be raised errors:

- `EnvironmentError: mysql_config not found` <http://stackoverflow.com/questions/5178292/pip-install-mysql-python-fails-with-environmenterror-mysql-config-not-found>, it seems mysql_config is missing on your system or the installer could not find it. Be sure mysql_config is really installed. For example on debian you must install the package: libmysqlclient-dev.  Maybe the mysql_config is not in your path, it will be the case when you compile by yourself the mysql suite.

    sudo apt-get install libmysqlclient-dev

- fatal error: Python.h: No such file or directory <http://www.cyberciti.biz/faq/debian-ubuntu-linux-python-h-file-not-found-error-solution/>. Please check that python-dev is installed

    sudo apt-get install python-dev
    
