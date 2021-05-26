#!/usr/bin/env python

from __future__ import absolute_import
import sys
import os
import os.path
import platform
import struct
import shutil
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

this_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_dir)

setup_args = dict(
    name='omniorb',
    version='4.2.4',
    description='Python bindings for omniORB',
    long_description='Python bindings for omniORB',
    author='Duncan Grisby et al',
    author_email='duncan@grisby.org',
    url='https://github.com/metamorph-inc/omniORB',
    license='LGPL for libraries, GPL for tools',

    packages=['omniORB'],
    package_dir = {'': 'omniORB/src/lib/omniORBpy/' + ('python' if sys.version_info[0] == 2 else 'python3')},
    # package_data={"omniORB": [r"omniORB\bin\x86_win32\omniORB424_vc14_rt.dll"]},
    data_files=[("lib\\site-packages", [r"omniORB\bin\x86_win32\omniORB424_vc14_rt.dll", r"omniORB\bin\x86_win32\omnithread41_vc14_rt.dll"])],

)

setup_args['ext_modules'] = [
    Extension(name,
              ['_build_with_make.cpp'],
              libraries=['omniorb'],
              ) for name in  ['_omnipy', '_omniConnMgmt', '_omnicodesets',
# FIXME do we need this or others: _omnisslTP
]]

if platform.system() == 'Windows':
    class my_build_ext(build_ext):
        def build_extension(self, ext):
            # shutil.copyfile(os.path.join(this_dir, r'' % sys.version_info[0:2]), self.get_ext_fullpath(ext.name))
            shutil.copyfile(os.path.join(this_dir, 'omniORB/lib/x86_win32/{}.pyd'.format(ext.name)), self.get_ext_fullpath(ext.name))

    setup_args['cmdclass'] = {'build_ext': my_build_ext}
else:
    raise ValueError('non-Windows platforms are unimplemented')

setup(**setup_args)
