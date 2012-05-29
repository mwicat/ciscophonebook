from setuptools import setup

import os, glob

def read(fname):
    return open(fname).read()

setup(
    name = "pyciscofon",
    version = "0.0.1",
    author = "Marek Wiewiorski",
    author_email = "mwicat@gmail.com",
    description = (""),
    license = "BSD",
    packages=['skinnyproxy'],
    install_requires = ['ldap', 'flask'],
    long_description=read('README'),
    entry_points = {
        'console_scripts': [
            ]
        },

