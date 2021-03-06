"""
Build script for TaskMaster.
"""
import glob
from setuptools import setup
import sys

mainscript = 'main.py'
data = [('Assets', glob.glob('Assets/*.*'))]

if sys.platform == 'darwin':

    OPTIONS = {
        'argv_emulation': True,
        'site_packages': True,
        'iconfile': 'TM.ico',
        'packages': []
    }

    setup(
        name='TaskMaster',
        version='1.0.0',
        description='A python-based application that can run common psych research tasks on any system using PyQt.',
        author='David Michael Nolta Garavito',
        author_email='d.garavito2@gmail.com',
        setup_requires=['py2app', 'PyQt6', 'numpy', 'scipy', 'pandas', 'xlsxwriter', 'adopy'],
        app=[mainscript],
        options={'py2app': OPTIONS}
    )

if sys.platform == 'win32':

    setup(
        name='TaskMaster',
        version='1.0',
        description='A python-based application that can run common psych research tasks on any system using PyQt.',
        author='David Michael Nolta Garavito',
        author_email='d.garavito2@gmail.com',
        setup_requires=['PyQt6', 'numpy', 'scipy', 'pandas', 'xlsxwriter', 'adopy'],
        app=[mainscript]
    )
