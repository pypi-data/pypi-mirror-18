#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages, Extension

extensions = [
    Extension('cycloudpickle.cycloudpickle', ['cycloudpickle/cycloudpickle.pyx']),
    Extension('cycloudpickle.cypickle', ['cycloudpickle/cypickle.pyx']),
]

try:
    from Cython.Build import cythonize
    extensions = cythonize(extensions, compiler_directives={
        'language_level': 3
    })
except ImportError:
    pass


if __name__ == '__main__':
    setup(
        name='cycloudpickle',
        version='0.1.0',
        url='https://github.com/bndl/cycloudpickle',
        description='A cython version of cloudpickle',
        long_description=open('README.rst').read(),
        author='Frens Jan Rumph',
        author_email='mail@frensjan.nl',

        packages=(
            find_packages()
        ),

        include_package_data=True,
        zip_safe=False,

        install_requires=[
            'cloudpickle>=0.2.1',
        ],
        extras_require=dict(
            dev=[
                'cython<0.25',
                'pytest',
                'mock',
                'tornado',
            ],
        ),

        ext_modules=extensions,

        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
    )
