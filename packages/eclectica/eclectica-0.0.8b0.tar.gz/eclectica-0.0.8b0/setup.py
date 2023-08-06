#!/usr/bin/env python

from distutils.core import setup
from subprocess import call
import os
import sys
import os.path

from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools import setup, find_packages

def download():
  # Make a copy of the current environment
  env = {
    'EC_VERSION': '0.0.8',
    'EC_DEST': os.path.dirname(sys.executable)
  }

  call(["./scripts/install.sh"], env=env)

class PostDevelopCommand(develop):
  def run(self):
    download()

class PostInstallCommand(install):
  def run(self):
    download()

setup(
  name = 'eclectica',
  package_data={
      'scripts': ['scripts/install.sh'],
   },
  version = '0.0.8b',
  description = 'Cool and eclectic version manager for any language',
  author = 'Oleg Gaidarenko',
  author_email = 'markelog@gmail.com',
  url = 'https://github.com/markelog/eclectica',
  license = 'MIT',
  include_package_data=True,
  zip_safe=False,
  keywords = [
    'eclectica',
    'version',
    'manager',
    'binary',
    'environment'
  ],
  classifiers = [],
  cmdclass = {
    'develop': PostDevelopCommand,
    'install': PostInstallCommand,
  },
)
