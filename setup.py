import sys
import kvlite

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'kvlite',
    version = kvlite.__version__,
    author = 'Andrey Usov',
    author_email = 'ownport@gmail.com',
    url = 'https://github.com/ownport/kvlite',
    description = ("key-value database wrapper for SQL database (MySQL, SQLite) "),
    long_description = open('README.rst').read(),
    license = "BSD",
    keywords = "key-value python database mysql sqlite wrapper",
    packages = ['kvlite', 'kvlite.webui'],
    include_package_data = True,
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules'
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
