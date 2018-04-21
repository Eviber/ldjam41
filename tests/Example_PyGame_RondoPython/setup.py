# -*- coding: utf-8 -*-
"""
Created on Sun Feb 09 19:58:35 2014

@author: Lexou
"""

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': "platformer.py"}],
    zipfile = None,
)