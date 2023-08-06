#!/usr/bin/env python
# encoding: utf-8
# Copyright (C) 2015 John Törnblom
import logging
import unittest
import sys

try:
    from setuptools import setup
    from setuptools import Command
    from setuptools.command.build_py import build_py
except ImportError:
    from distutils.core import setup
    from distutils.core  import Command
    from distutils.command.build_py import build_py

import xtuml
from bridgepoint import oal


logging.basicConfig(level=logging.DEBUG)


class BuildCommand(build_py):
    
    def run(self):
        l = xtuml.ModelLoader()
        l.input('', name='<empty string>')
        l.build_metamodel()
        oal.parse('')
        build_py.run(self)


class TestCommand(Command):
    description = "Execute unit tests"
    user_options = [('name=', None, 'Limit testing to a single test case or test method')]

    def initialize_options(self):
        self.name = None
    
    def finalize_options(self):
        if self.name and not self.name.startswith('tests.'):
            self.name = 'tests.' + self.name

    def run(self):
        if self.name:
            suite = unittest.TestLoader().loadTestsFromName(self.name)
        else:
            suite = unittest.TestLoader().discover('tests')
        
        runner = unittest.TextTestRunner(verbosity=2, buffer=True)
        exit_code = not runner.run(suite).wasSuccessful()
        sys.exit(exit_code)


setup(name='pyxtuml',
      version=xtuml.version.release,
      description='Library for parsing, manipulating, and generating BridgePoint xtUML models',
      author='John Törnblom',
      author_email='john.tornblom@gmail.com',
      url='https://github.com/xtuml/pyxtuml',
      license='GPLv3',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Code Generators',
          'Topic :: Software Development :: Compilers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5'],
      keywords='xtuml bridgepoint',
      packages=['xtuml', 'bridgepoint'],
      requires=['ply'],
      cmdclass={'build_py': BuildCommand,
                'test': TestCommand}
      )

