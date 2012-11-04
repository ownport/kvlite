#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   kvlite console
#
#
__author__ = 'Andrey Usov <https://github.com/ownport/kvlite>'
__version__ = '0.3'
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

import cmd
import kvlite
import pprint

# -----------------------------------------------------------------
# Console class
# -----------------------------------------------------------------
class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "kvlite> "
        self.ruler = '-'

        self.__history_size = 20
        self.__history = list()
        self.__kvlite_colls = dict()
        self.__current_coll_name = None
        self.__current_coll = None

    def emptyline(self):
        return False
    
    def do_help(self, arg):
        '''   help <command>\tshow <command> help'''
        if arg:
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc=getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n"%str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n"%str(self.nohelp % (arg,)))
                return
        else:
            names = [
                '', 'do_help', 'do_version', 'do_licence', 'do_history', 'do_exit', '',
                'do_create', 'do_use', 'do_show', 'do_remove', 'do_import', 'do_export', '',
                'do_hash', 'do_items', 'do_get', 'do_put', 'do_delete', 
                'do_count', 'do_scheme', 'do_index', ''
            ]
            for name in names:
                if not name:
                    print
                else:
                    print getattr(self, name).__doc__

    def do_history(self,line):
        '''   history\t\tshow commands history '''
        for i, line in enumerate(self.__history):
            print "0%d. %s" % (i+1, line) 

    def precmd(self, line):
        if len(self.__history) == self.__history_size:
            prev_line = self.__history.pop(0)
        if line and line not in self.__history:
            self.__history.append(line)
        return line

    def do_version(self, line):
        '''   version\t\tshow kvlite version'''
        print 'version: %s' % __version__

    def do_licence(self, line):
        '''   licence\t\tshow licence'''
        print __license__
        print

    def do_exit(self, line):
        '''   exit\t\t\texit from console '''
        return True

    def do_import(self, filename):
        '''   import <filename>\t\timport collection configuration from JSON file'''
        import os
        import json
        
        if not filename:
            print getattr(self, 'do_import').__doc__
            return
        filename = filename.rstrip().lstrip()
        
        if os.path.isfile(filename):
            for k, v in json.loads(open(filename).read()).items():
                self.__kvlite_colls[k] = v
            print 'Import completed'
        else:
            print 'Error! File %s does not exists' % filename

    def do_export(self, filename):
        '''   export <filename>\t\texport collection configurations to JSON file'''
        import json
        
        if not filename:
            print getattr(self, 'do_import').__doc__
            return
        filename = filename.rstrip().lstrip()
        json_file = open(filename, 'w')
        json_file.write(json.dumps(self.__kvlite_colls))
        json_file.close()
        print 'Export completed to file: %s' % filename

    def do_show(self, line):
        '''   show collections <details>\tlist of available collections (defined in settings.py)'''
        if line.startswith('collections'):

            for coll in self.__kvlite_colls:
                print '   %s' % coll
        else:
            print 'Unknown argument: %s' % line
    
    def do_use(self, collection_name):
        '''   use <collection_name>\tuse the collection as the default (current) collection'''
        if collection_name in self.__kvlite_colls:
            self.prompt = '%s>' % collection_name
            self.__current_coll_name = collection_name
            self.__current_coll = kvlite.open(self.__kvlite_colls[self.__current_coll_name])
            return
        else:
            print 'Error! Unknown collection: %s' % collection_name

    def do_create(self, line):
        '''   create <name> <uri>\t\tcreate new collection (if not exists)'''
        try:
            name, uri = [i for i in line.split(' ') if i <> '']
        except ValueError:
            print getattr(self, 'do_create').__doc__
            return
            
        if name in self.__kvlite_colls:
            print 'Warning! Collection name already defined in the list: %s, %s' % (name, self.__kvlite_colls[name]) 
            print "If it's needed please change collection name"
            return
        try:
            manager = kvlite.CollectionManager(uri)
            params = manager.parse_uri(uri)
            if params['collection'] in manager.collections():
                self.__kvlite_colls[name] = uri
                print 'Connection exists, the reference added to collection list'
                return
            else:
                manager.create(params['collection'])
                self.__kvlite_colls[name] = uri
                print 'Collection created and added to collection list'
                return
        except Exception, err:
            print 'Error! Incorrect URI: %s' % uri
            return
        except ConnectionError, err:
            print 'Connection Error! Please check URI, %s' % str(err)
            return

    def do_remove(self, name):
        '''   remove <collection_name>\tremove collection'''
        if name not in self.__kvlite_colls:
            print 'Error! Collection name does not exist in the list: %s' % name
            return
        try:
            uri = self.__kvlite_colls[name]
            manager = kvlite.CollectionManager(uri)
            params = manager.parse_uri(uri)
            if params['collection'] in manager.collections():
                manager.remove(params['collection'])
                del self.__kvlite_colls[name]
                print 'Collection %s deleted' % name
                return
            else:
                print 'Error! Collection does not exist, %s' % self.__kvlite_colls[name]
        except Exception, err:
            print 'Error! %s' % err
            return

    def do_scheme(self, line):
        '''   scheme\t\tshow structure of collection'''
        if not self.__current_coll_name in self.__kvlite_colls:
            print 'Error! Unknown collection: %s' % self.__current_coll_name
            return
        print 'Building ...'
        doc_struct = kvlite.docs_struct(self.__current_coll.get())
        if doc_struct:
            pprint.pprint(doc_struct)
        print 'Done'

    def do_hash(self, line):
        '''   hash [string]\tgenerate sha1 hash, random if string is not defined'''        
        import hashlib
        import datetime
        if not line:
            str_now = str(datetime.datetime.now())
            print 'Random sha1 hash:', hashlib.sha1(str_now).hexdigest()
        else:
            line = line.rstrip().lstrip()
            print 'sha1 hash:', hashlib.sha1(line).hexdigest()
        
    def do_items(self, line):
        '''   items\t\tlist of collection's items '''        
        if not self.__current_coll_name in self.__kvlite_colls:
            print 'Error! Unknown collection: %s' % self.__current_coll_name
            return
        for k,v in self.__current_coll.get():
            print '_key:', k
            pprint.pprint(v)
            print
        
    def do_count(self, args):
        '''   count\t\tshow the amount of entries in collection '''        
        if self.__current_coll:
            print self.__current_coll.count

    def do_get(self, key):
        '''   get <key>\t\tshow collection entry by key'''    
        if not key:
            print getattr(self, 'do_get').__doc__
            return
        for key in [k for k in key.split(' ') if k <> '']:
            if self.__current_coll:
                k, v = self.__current_coll.get({'_key': key})
                print '_key:', k
                pprint.pprint(v)
                print
            else:
                print 'Error! The collection is not selected, please use collection'
                return
    
    def do_put(self, line):
        '''   put <key> <value>\tstore entry to collection'''

        try:
            k,v = [i for i in line.split(' ',1) if i <> '']
        except ValueError:
            print getattr(self, 'do_put').__doc__
            return

        if self.__current_coll:
            try:
                self.__current_coll.put(k, v)
                self.__current_coll.commit()
                print 'Done'
                return
            except WronKeyValue, err:
                print 'Error! Incorrect key/value,', err
                return 
        else:
            print 'Error! The collection is not selected, please use collection'
            return


    def do_delete(self, key):
        '''   delete <key>\t\tdelete entry by key '''
        key = key.rstrip().lstrip()
        try:
            if self.__current_coll.get(key) <> (None, None):
                self.__current_coll.delete(key)
                self.__current_coll.commit()
                print 'Done'
                return
            else:
                print 'Error! The key %s does not exist' % key
                return        
        except RuntimeError, err:
            print 'Error!', err
            return

    def do_index(self, line):
        '''   index <details>\tmake index for current collection'''
        print 'Warning! This functionality is not implemented yet'
        print line
        print 'Done'
        
# ----------------------------------
#   main
# ----------------------------------
if __name__ == '__main__':
    console = Console()
    console.cmdloop()


