# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


# package settings
setup(

    # info
    name='rxvpntoggle',
    version='0.0.1',
    author='Alden',
    url='https://github.com/aldencolerain/rxvpntoggle.git',
    description='VPN toggle for indicator for Xubuntu.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    # include
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,

    # public dependencies
    install_requires=['PyGObject >= 3'],

    # keep this package private
    classifiers=['Private :: Do Not Upload'],

    # cli scripts
    entry_points={'console_scripts': ['rxvpntoggle = rxvpntoggle.cli:main']},
)
