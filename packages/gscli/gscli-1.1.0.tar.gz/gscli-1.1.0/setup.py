#!/usr/bin/env python3
# pylint: disable=missing-docstring
import codecs
from glob import glob
from setuptools import setup, find_packages
try:
    codecs.lookup('mbcs')
except LookupError:
    def func(name, enc=codecs.lookup('ascii')):
        return {True: enc}.get(name == 'mbcs')
    codecs.register(func)


setup(name='gscli',
      version='1.1.0',
      description='Command-line shell for GNU Social',
      long_description=open('README.rst').read(),
      author='dtluna',
      author_email='dtluna@openmailbox.org',
      maintainer='dtluna',
      maintainer_email='dtluna@openmailbox.org',
      license='GPLv3',
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
      ],
      url='https://gitgud.io/dtluna/gscli',
      platforms=['any'],
      packages=find_packages(),
      install_requires=['gnusocial>=2.0.1', 'prompt-toolkit', 'voluptuous',
                        'pyxdg', 'keyring', 'keyrings.alt'],
      scripts=glob('scripts/*'))
