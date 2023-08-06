#!/usr/bin/env python

from setuptools import setup, find_packages

requires = [
    'docker-py',
    'enum34',
    'future',
    'six',
    'PyYaml',
    'requests'
]

setup(name='versioner-cli',
      version='1.0.25',
      description='cli tool to interact with versioner service',
      author='Ben Waters',
      author_email='ben@book-md.com',
      package_dir={'': 'lib'},
      packages=find_packages('lib'),
      data_files=[('/etc/default', ['config/versioner'])],
      license='MIT',
      url="https://github.com/bookmd/bookmd-versioner-cli",
      scripts=['bin/versioner-cli'],
      install_requires=requires,
      )
