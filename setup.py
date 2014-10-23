#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import io
import os
import sys


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

about={}
initfile = os.path.join(here, 'src', 'jukeboxcore', '__init__.py')
with open(initfile) as fp:
    exec(fp.read(), about)

long_description = read('README.rst', 'HISTORY.rst')
install_requires = ['pyside', 'configobj', 'django>=1.7', 'psycopg2']
tests_require = ['pytest', 'nose']


setup(
    name='jukebox-core',
    version=about['__version__'],
    description='Core package for the jukebox pipeline.',
    long_description=long_description,
    author=about['__author__'],
    author_email=about['__email__'],
    url='https://github.com/JukeboxPipeline/jukebox-core',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'jukeboxcore': ['data/*.*']},
    include_package_data=True,
    tests_require=tests_require,
    install_requires=install_requires,
    cmdclass={'test': PyTest},
    license='BSD',
    zip_safe=False,
    keywords='jukebox-core',
    entry_points={
        'console_scripts': [
            'jukebox = jukeboxcore.launcher:main_func',
        ],
        'gui_scripts': [
            'jukeboxw = jukeboxcore.launcher:main_func',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
)
