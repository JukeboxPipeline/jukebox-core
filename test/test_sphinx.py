""" This file tests the sphinx-build """

import py
from os import path
import subprocess


class Test_SphinxBuild(object):
    """Test sphinx build by wrapping sphinx build 
       commands into a test class
    """

    def __init__(self, tmpdir):
        """Setup environment variables

        :param tmpdir: a pytest fixture pointing to a temp directory
        """

        self.doctreedir = path.join(__file__, "..", "docs") 
        self.htmldir    = path.join(tmpdir, "dist", "docs") 

    def test_linkcheck(self):
        """performs a linkcheck on sphinx build """

        subprocess.check_call(
            ["sphinx-build", "-b", "linkcheck",
              str(self.doctreedir), str(htmldir)])
    
    def test_build_docs(self):
        """Performs a build check using sphinx build """

        subprocess.check_call([
            "sphinx-build", "-b", "html",
              str(self.doctreedir), str(htmldir)])