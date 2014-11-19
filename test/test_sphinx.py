""" This file tests the sphinx-build """

import py
import subprocess
def test_linkcheck(tmpdir):
    doctrees = tmpdir.join("docs")
    htmldir = tmpdir.join("dist/docs")
    subprocess.check_call(
        ["sphinx-build", "-b", "linkcheck",
          "-d", str(doctrees), str(htmldir)])
def test_build_docs(tmpdir):
    doctrees = tmpdir.join("docs")
    htmldir = tmpdir.join("dist/docs")
    subprocess.check_call([
        "sphinx-build", "-b", "html",
          "-d", str(doctrees), str(htmldir)])
