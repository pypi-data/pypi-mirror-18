#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


requirements = [
# "Lasagne==0.1", "matplotlib==1.5.3", "numpy", "Theano==0.8.2"
"matplotlib==1.5.3", "numpy"
]


test_requirements = requirements


setup(
    name='lasagne_visualizer',
    version='0.1.0',
    description="A tiny package to enable live-visualization of weight learning using lasagne models in ipython notebook.",
    long_description=readme + '\n\n' + history,
    author="Simon Kohl",
    author_email='simon.kohl@dkfz.de',
    url='https://github.com/SimonKohl/lasagne_visualizer',
    packages=[
        'lasagne_visualizer',
    ],
    package_dir={'lasagne_visualizer':
                 'lasagne_visualizer'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='lasagne_visualizer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
