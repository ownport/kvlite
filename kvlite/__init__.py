#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   Simple key-value datastore

#   some ideas taked from PyMongo interface http://api.mongodb.org/python/current/index.html
#   kvlite2 tutorial http://code.google.com/p/kvlite/wiki/kvlite2
#
__author__ = 'Andrey Usov <https://github.com/ownport/kvlite>'
__version__ = '0.6.0'
__license__ = """
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

import os
import sys
import binascii

from kvlite.utils import open
from kvlite.utils import remove
from kvlite.utils import get_uuid
from kvlite.utils import dict2flat
from kvlite.utils import docs_struct

from kvlite.serializers import cPickleSerializer
from kvlite.serializers import CompressedJsonSerializer

__version__ = 'v0.6.0'


__all__ = [
    'open', 'remove', 'get_uuid', 'dict2flat', 'docs_struct',
    'BaseCollection', 'BaseCollectionManager',
    'CollectionManager',
    'CompressedJsonSerializer', 'cPickleSerializer',
    'MysqlCollection', 'SqliteCollection',
    'MysqlCollectionManager', 'SqliteCollectionManager',
]




   

       
