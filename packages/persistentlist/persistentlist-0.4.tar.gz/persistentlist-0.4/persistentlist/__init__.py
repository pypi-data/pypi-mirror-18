# -*- coding: utf-8 -*-
# Copyright © 2016 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
    The ``persistentlist`` module
    =============================
 
    The persistentlist module provides classes to use a PersistentList.
 
    :Example:
 
    >>> from persistentlist import PersistentList
    >>> cache = PersistentList('cache', 3)
    >>> cache.append(1)
    >>> cache
    [1]
    >>> cache.append(2)
    >>> cache
    [1, 2]
    >>> cache.append(3)
    >>> cache
    [1, 2, 3]
    >>> cache.append(4)
    >>> cache
    [2, 3, 4]

"""

# standard libraries imports
import errno
import os
import os.path
import shelve
import sys

class PersistentList(object):
    '''
        The PersistentList class. Instantiate a PersistentList object.

        :param dbpath: The path to the cache file. Defaults to 'cache'.
        :type protocol: str
        :param maxitems: The maximum number of elements in your PersistentList. Defaults to 0 for no maximum.
        :return: A PersistentList object
        :rtype: PersistentList

        :Example:
 
        >>> from persistentlist import PersistentList
        >>> cache = PersistentList('cache', 3)
        >>> cache
        []
        >>> type(cache)
        <class 'persistentlist.PersistentList'>

    '''


    def __init__(self, dbpath='cache', maxitems=0):
        self.dblist = []
        self.maxitems = maxitems
        self.dbpath = dbpath
        self.main()

    def __enter__(self):
        self.main()
        return self

    def __exit__(self, *args):
        self.close()

    def main(self):
        extension = 'db'
        # use only absolute path
        if not os.path.isabs(self.dbpath):
            self.dbpath = os.path.abspath(self.dbpath)
        dbpathwithext = '.'.join([self.dbpath, extension])
        # test the path
        pathhead, pathtail = os.path.split(self.dbpath)
        # raise OSError if the absolute path to the parent directory
        # of the file we need does not exist, meaning you cannot create it
        if not os.path.exists(pathhead):
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), pathhead)
        # parent directory exists but not the file, so we create it
        if not os.path.exists(dbpathwithext):
            self.db = shelve.open(self.dbpath, writeback=True)
            self.db['itemlist'] = []
        else:
            self.db = shelve.open(self.dbpath, writeback=True) 

    def __str__(self):
        return self.db['itemlist'].__repr__()

    def __repr__(self):
        return str(self.db['itemlist'])

    def __iter__(self):
        for elem in self.db['itemlist']:
            yield elem

    def append(self, item):
        '''
            Append a new element at the end of the PersistentList object.
            When the max size of the PersistentList is reached, the first element is dropped

            :param item: An item to append at the end of the PersistentList element.

            :Example:
     
            >>> from persistentlist import PersistentList
            >>> cache = PersistentList('cache', 3)
            >>> cache
            []
            >>> cache.append(1)
            >>>

        '''
        if self.maxitems and len(self.db['itemlist']) == self.maxitems:
            del self.db['itemlist'][0]
        self.db['itemlist'].append(item)

    def extend(self, items):
        '''
            Extend a PersistentList object with a list of elements.
            When the max size of the PersistentList is reached, the first element is dropped

            :param items: List of items to append at the end of the PersistentList object.

            :Example:
     
            >>> from persistentlist import PersistentList
            >>> cache = PersistentList('cache', 3)
            >>> cache.extend([1,2,3])
            >>> cache
            [1,2,3]

        '''
        for item in items:
            self.append(item)

    def close(self):
        '''
            Close a PersistentList object.

            :Example:
     
            >>> from persistentlist import PersistentList
            >>> cache = PersistentList('cache', 3)
            >>> cache.close()
            >>>

        '''
        self.db.close()
