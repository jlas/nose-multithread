#!/usr/bin/env

from setuptools import setup

setup(
    name = 'nosemultithread',
    version = '0.0.1',
    author = 'Juan Lasheras',
    author_email = 'juan.lasheras@gmail.com',
    description = ('nose plugin for multi-threaded testing'),
    long_description = \
    """nose plugin for multi-threaded testing
    """,
    license = 'GNU LGPL',
    keywords = 'test nose multithread',
    packages = ['nosemultithread'],
    entry_points = {
        'nose.plugins.0.10': [
            'multithread = nosemultithread:MultiThread'
            ]
        }
    )

