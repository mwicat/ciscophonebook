from setuptools import setup

import os, glob

def read(fname):
    return open(fname).read()

setup(
    name = "cisco_ldap",
    version = "0.0.1",
    author = "Marek Wiewiorski",
    author_email = "mwicat@gmail.com",
    description = (""),
    license = "BSD",
    packages=['phoneldap'],
    install_requires = ['pycisco', 'python-ldap', 'flask'],
    package_data = { '': [ 'templates/*.xml' ] },
    long_description=read('README'),
    entry_points = {
        'console_scripts': [
            'cisco_ldap = phoneldap.webapp:main',
            ]
        }
)
