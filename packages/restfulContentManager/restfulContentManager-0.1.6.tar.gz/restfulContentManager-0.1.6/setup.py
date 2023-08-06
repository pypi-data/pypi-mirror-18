#! /usr/bin/env python3

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='restfulContentManager',
    version='0.1.6',
    description='A ContentManager for IPython/Jupyter that queries a restful API for entries.',
    author='DataScience',
    author_email='dev@datascience.com',
    url='https://github.com/datascienceinc/RestfulContentManager',
    download_url='https://github.com/datascienceinc/RestfulContentManager/tarball/0.0.0',
    packages=find_packages(exclude=['example', 'tests']),
    install_requires=[
        'mixpanel',
        'notebook',
        'requests',
        'tornado',
        'traitlets',
    ]
)
