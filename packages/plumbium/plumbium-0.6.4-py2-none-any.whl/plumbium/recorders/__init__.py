"""
plumbium.recorders
==================

Module containing functions for recording results to files and databases.
"""

from __future__ import absolute_import
from .csvfile import CSVFile
from .sqldatabase import SQLDatabase
from .mongodb import MongoDB
from .stdout import StdOut
from .slack import Slack
