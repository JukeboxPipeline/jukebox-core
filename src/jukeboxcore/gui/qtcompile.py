import os
import subprocess

import pysideuic
import PySide

import jukeboxcore.gui.resources


def compile_ui(uifile):
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


def compile_rcc(rccfile):
    """Compile the given Qt resource file. The compiled file will be in the jukeboxcore.gui.resources package and ends with _rc.py

    :param rccfile: filepath to the rccfile
    :type rccfile: str
    :returns: None
    :rtype: Nonen
    :raises: None
    """
    print "Compileing: %s" % rccfile
    rccfilename = os.path.basename(rccfile)
    outname = rccfilename.rsplit(os.path.extsep, 1)[0] + "_rc.py"
    # put in resoures package
    path = os.path.dirname(jukeboxcore.gui.resources.__file__)
    outputpath = os.path.join(path, outname)
    print "Outputfile: %s" % outputpath
    # get pyside-rcc.exe. It is in the PySide dir.
    pysidedir = os.path.dirname(PySide.__file__)
    pysidercc = os.path.join(pysidedir, "pyside-rcc.exe")
    args=[pysidercc, "-o", outputpath, rccfile]
    rc = subprocess.call(args)
    print "Finished with returncode %s" % rc
