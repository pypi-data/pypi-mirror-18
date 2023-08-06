# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, pip
from subprocess import Popen, PIPE

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from scriptler import __version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()

def sh(*args):
    return Popen(args, stdout=PIPE).communicate()[0].strip().decode()

def current_commit():
    return sh('git', 'rev-parse', '--short', 'HEAD')

def last_git_tag():
    return sh('git', 'describe', '--abbrev=0', '--tags')

def git_tag_for(commit):
    return sh('git', 'tag', '--points-at', commit)

def git_version():
    commit = current_commit()
    tag = git_tag_for(commit)

    if not tag:
        # this is not PEP440 compatible
        return '{0}-{1}'.format(last_git_tag(), commit)

    if tag and tag != __version__:
        raise Exception('internal version {} is not equal to deployed version {}'.format(__version__, tag))

    return tag

install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

requirements = [str(ir.req) for ir in install_reqs if ir is not None]

version = git_version()

setup(name             = "scriptler",
      author           = "Aljosha Friemann",
      author_email     = "aljosha.friemann@gmail.com",
      description      = "manage scripts from different sources",
      license          = read('LICENSE.txt'),
      long_description = read('README.rst'),
      url              = "https://www.github.com/afriemann/scriptler",
      download_url     = "https://github.com/AFriemann/scriptler/archive/{}.tar.gz".format(version),
      keywords         = ['scripts'],
      version          = version,
      install_requires = requirements,
      classifiers      = [],
      packages         = ["scriptler"],
      package_data     = { 'scriptler': ['VERSION'] },
      entry_points     = { 'console_scripts': ['scriptler=scriptler.cli:run'] },
      platforms        = 'linux'
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
