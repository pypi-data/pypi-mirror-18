# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

setup(
    name='densratio',
    version='0.1.1',
    description='A Python Package for Density Ratio Estimation',
    long_description='A Python Package for Density Ratio Estimation',
    author='Koji Makiyama',
    author_email='hoxo.smile@gmail.com',
    install_requires=['numpy'],
    url='https://github.com/hoxo-m/densratio_py',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)
