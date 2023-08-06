#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2016 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


import sys
from pkg_resources import iter_entry_points

from .database import Database

DATABASES = dict()
TASKS = dict()

for o in iter_entry_points(group='pyannote.database.databases', name=None):

    database_name = o.name

    DatabaseClass = o.load()
    DATABASES[database_name] = DatabaseClass

    database = DatabaseClass()

    for task in database.get_tasks():
        if task not in TASKS:
            TASKS[task] = set()
        TASKS[task].add(database_name)

    setattr(sys.modules[__name__], database_name, DatabaseClass)


def get_databases(task=None):
    """List of databases

    Parameters
    ----------
    task : str, optional
        Only returns databases providing protocols for this task.
        Defaults to return every database.

    Returns
    -------
    databases : list
        List of database, sorted in alphabetical order

    """

    if task is None:
        return sorted(DATABASES)

    return sorted(TASKS.get(task, []))


def get_database(database_name, **kwargs):
    """Get database by name

    Parameters
    ----------
    name : str
        Database name.

    Returns
    -------
    Database : Class
        Database class.
    """
    return DATABASES[database_name](**kwargs)


def get_tasks():
    """List of tasks"""
    return sorted(TASKS)


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
