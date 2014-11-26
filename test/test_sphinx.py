""" This file tests the sphinx-build """
from os import path
import subprocess

import pytest


@pytest.fixture(scope='module')
def doctreedir():
    """Return the dir of the documenation
    """
    return path.join(path.dirname(__file__), "..", "docs")


@pytest.fixture(scope='function')
def htmldir(tmpdir):
    """Return a path for building the sphinx documentation

    :param tempdir: pytest fixture for a temporary dir
    :type tempdir: str
    :returns: the path. a tempdir path
    :rtype: str
    :raises: None
    """
    return tmpdir.mkdir("dist").mkdir("docs").strpath


def test_linkcheck(doctreedir, htmldir):
    """performs a linkcheck on sphinx build """
    subprocess.check_call(
        ["sphinx-build", "-b", "linkcheck",
         str(doctreedir), str(htmldir)])


def test_build_docs(doctreedir, htmldir):
    """Performs a build check using sphinx build """
    subprocess.check_call([
        "sphinx-build", "-b", "html",
        str(doctreedir), str(htmldir)])
