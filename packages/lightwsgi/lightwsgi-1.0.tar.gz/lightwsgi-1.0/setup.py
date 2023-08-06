# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import urllib2, shutil, os

setup(
    name='lightwsgi',
    version="1.0",
    packages=find_packages(),
    include_package_data=False,
    install_requires=[],
    author="Louis Young",
    author_email="louispryoung@gmail.com",
    description="A small, simple and lightweight WSGI framework and helpers.",
    keywords=["wsgi", "framework", "lightweight", "apache"],
)
