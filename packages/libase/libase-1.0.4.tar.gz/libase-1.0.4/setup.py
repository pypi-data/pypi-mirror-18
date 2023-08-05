#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   setup.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import os

from setuptools import (
    setup,
    )

VERSION = '1.0'

def main():
    # 版本
    subversion = os.environ.get('SUBVERSION', '').strip()
    if subversion:
        version = '.'.join([VERSION, subversion])
    else:
        version = VERSION

    setup(
        name='libase',
        version=version,
        author='Fasion Chan',
        author_email='fasionchan@gmail.com',
        packages=[
            'libase',
            'libase.client',
            'libase.multirun',
            'libase.platform',
            'libase.platform.syscall',
            'libase.server',
            'libase.util',
            'libase.vendor',
            'libase.vendor.douban',
            ],
        scripts=[
            ],
        package_data={
            },
        install_requires=[
            ],
        )

if __name__ == '__main__':
    main()
