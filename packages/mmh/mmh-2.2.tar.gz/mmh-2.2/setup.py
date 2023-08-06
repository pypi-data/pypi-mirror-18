#!/usr/bin/env python
#! coding: utf-8

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

extra_compile_args = ['-g', '-fPIC', '-Wall', '-O2']

setup(
    name='mmh',
    version='2.2',
    maintainer='Michael Lee',
    maintainer_email='liyong19861014@gmail.com',
    url='https://github.com/airhuman/py_mmh.git',
    description='Python bindings for Google Murmurhash2 hash algorithm',
    packages=['mmh'],
    ext_modules=[
        Extension(
            'mmh.hash_f', sources=['mmh/hash_f.c'],
            extra_compile_args=extra_compile_args)
    ],
    entry_points={
        'console_scripts': [
            'echo_mmh_version = mmh.mmh_version:main',
        ],
    }
)
