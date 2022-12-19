#!/usr/bin/env python
NAME = 'Iaji'
AUTHOR = 'Iyad Suleiman'
AUTHOR_EMAIL = 'jiedz@protonmail.com'
DESCRIPTION = 'Utility packages of various types (mathematics, physics, instrument control, signal processing, GUI, ...)'
PLATFORMS = ['all']
REQUIREMENTS = ['numpy', 'scipy', 'sympy', 'symfit', 'matplotlib', 'pyqt5', 'signalslot', 'cloudpickle']

if __name__=='__main__':

    from setuptools import setup

    setup(
        name = NAME,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        description = DESCRIPTION,
        requirements = REQUIREMENTS,
        packages = ['Iaji'])
