from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='d3',
    version="0.1.0",
    description="A D3.js programming API for python",
    long_description=long_description,
    url="https://github.com/yuhangwang/d3-python",
    author="Yuhang(Steven) Wang",
    license="MIT/X11",
    packages=find_packages(),
    install_requires=[
        ],
    )
