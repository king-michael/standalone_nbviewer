#!/usr/bin/env python
"""
Install Script for the QtViewer
"""
from __future__ import print_function


import sys
import os
import stat

from shutil import copy2
import site
from argparse import ArgumentParser

assert sys.version_info.major >= 3, \
    "Not tested with Python {}.{}".format(sys.version_info.major, sys.version_info.minor)
assert os.path.normpath(sys.platform) == 'linux', \
    "Only tested for Linux (used platform : {})".format(os.path.normpath(sys.platform))


try:
    import PyQt5
except ModuleNotFoundError as e:
    print("No PyQt5 found. Please Install PyQt5 to use the qtviewer.py")


# Input
VERSION=0.1

files = {
    'qtviewer.py' : {
        '_output'     : 'jupyter-qtviewer.py',
        'Name'       : 'Jupyter-QtViewer',
        'Comment'    : 'QtViewer for Jupyter Notebooks',
        'Categories' : 'Viewer;',
        'Version'    : str(VERSION),
    },
    'browser.py' : {
        '_output'     : 'jupyter-browserviewer.py',
        'Name'       : 'Jupyter-BrowserViewer',
        'Comment'    : 'BrowserViewer for Jupyter Notebooks',
        'Categories' : 'Viewer;',
        'Version'    : str(VERSION),
    },
}

_template_desktop_file="""\
[Desktop Entry]
Version={Version}
Type=Application
Name={Name}
Exec="{path}" %f
Comment={Comment}
Categories={Categories}
Terminal=false
"""

# Argparser
parser = ArgumentParser(prog='install.py',
                        description='LAMMPS python module installer script')
parser.add_argument('-u',"--user", action='store_true',
                    help="Install in User Path")
parser.add_argument('-d','--with-desktop-files', action='store_true', help="Install Desktop Files")
args = parser.parse_args()


# Setup
install_desktop=args.with_desktop_files

if args.user:
    base=site.USER_BASE
else:
    base=os.path.normpath(sys.prefix)
if os.path.normpath(sys.platform) == 'linux':
    path_bin = os.path.join(base, 'bin')
    path_share_applications = os.path.join(base, 'share', 'applications')

here = os.path.abspath(os.path.dirname(__file__))


# Install
print('Install in {}'.format(base))
if not os.path.exists(path_bin):
    os.makedirs(path_bin)
if install_desktop and not os.path.exists(path_share_applications):
    os.makedirs(path_share_applications)

for fname, attrib in files.items():
    fname_exe=os.path.join(path_bin, attrib.get('_output', fname))
    print('  {} -> {}'.format(fname, fname_exe))
    copy2(os.path.join(here, fname), fname_exe)
    os.chmod(fname_exe, os.stat(fname_exe).st_mode | stat.S_IEXEC) # chmod +x

    if install_desktop:
        fname_desktop = os.path.join(path_share_applications, '{}.desktop'.format(os.path.splitext(attrib.get('_output', fname))[0]))
        print('  - create desktop file {}'.format(fname_desktop))
        with open(fname_desktop, 'w') as fp:
            fp.write(_template_desktop_file.format(path=fname_exe, **attrib))

if install_desktop:
    print('Run "update-desktop-database" to update your desktop files')