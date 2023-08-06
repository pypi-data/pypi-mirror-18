#!/usr/bin/env python
from setuptools import setup, find_packages

version = '1.0.1'

setup(
    name='api.mock',
    version=version,
    description='A utility of APIMock, push config files to Android device.',
    url='https://github.com/brucezz/APIMockHelper',
    author='Bruce Zheng',
    author_email='im.brucezz@gmail.com',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='adb python',
    packages=find_packages(),
    install_requires=[
        'docopt',
    ],
    entry_points={
        'console_scripts': [
            'api.mock = apimock.helper:main'
        ]
    },
)
