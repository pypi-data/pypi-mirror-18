#! /usr/bin/env python

import re

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

def read(file):
	with open(path.join(here, file), encoding='utf-8') as f:
		content = f.read()
	return content
	
def find_version(file):
	return re.search(r"__version__ = (\S*)", read(file)).group(1).strip("\"'")
	
setup(
    name         = "desktop3",
    description  = "Simple desktop integration for Python.",
    long_description = read("README.rst"),
    author       = "Paul Boddie",
    author_email = "paul@boddie.org.uk",
    maintainer = "eight04",
    maintainer_email = "eight04@gmail.com",
    url          = "https://github.com/eight04/pyDesktop3",
    version      = find_version("desktop/__init__.py"),
    packages     = find_packages(),
    license = "LGPLv3+",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Natural Language :: Chinese (Traditional)",
        "Environment :: MacOS X",
        "Environment :: Other Environment",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: Gnome",
        "Environment :: X11 Applications :: KDE",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Desktop Environment :: Window Managers :: XFCE",
        "Topic :: Utilities"
    ],
    keywords = "desktop startfile DESKTOP_LAUNCH KDE KDE4 GNOME XFCE XFCE4 Lubuntu dialog kdialog zenity Xdialog X11 start open opener launch launcher",
    platforms = "any"
)
