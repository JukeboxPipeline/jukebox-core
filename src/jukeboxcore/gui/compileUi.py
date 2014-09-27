#!/usr/bin/env python
"""Compile a ui file. For usage use::

  compileUi.py -h

The compiled file will be in the same directory but ends with _ui.py
This script uses pysideuic to compile the file.
"""
import os
import argparse

import pysideuic

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compiles Qt Designer Files')
    parser.add_argument('uifile',
                        help='the uifile that will be compiled. The compiled file will be in the same directory but ends with _ui.py',
                        type=argparse.FileType('r'))
    ns = parser.parse_args()
    uifile = ns.uifile.name
    outputpath = uifile.rsplit(os.path.extsep,1)[0]+'_ui.py'
    outputfile = open(os.path.abspath(outputpath), 'w')
    pysideuic.compileUi(os.path.abspath(uifile), outputfile)
