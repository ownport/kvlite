from setuptools import setup
import kvlite


setup (
    name = "kvlite",
    version = kvlite.__version__,
    author = kvlite.__author__,
    description = ("key-value database wrapper for SQL database (MySQL, SQLite) "),
    long_description = open('README.md').read(),
    license = "BSD",
    keywords = "key-value python database mysql sqlite",
    py_modules = ['kvlite', 'kvlite-cli'],
    data_files = [(os.path.join('share', 'urlfetch'), )],
    classifiers = [
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
