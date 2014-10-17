import os

import pysideuic


def compile(uifile):
    """Compile the given Qt designer file. The compiled file will be in the same directory but ends with _ui.py.

    :param uifile: filepath to the uifile
    :type uifile: str
    :returns: None
    :rtype: None
    :raises: None
    """
    print "Compileing: %s" % uifile
    outputpath = uifile.rsplit(os.path.extsep, 1)[0] + "_ui.py"
    print "Outputfile: %s" % outputpath
    outputfile = open(os.path.abspath(outputpath), "w")
    pysideuic.compileUi(os.path.abspath(uifile), outputfile)
    print "Done!"
