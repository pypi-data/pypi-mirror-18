# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='recaptcha-wrapper',
    version='0.01',
    description='Wrapper for Google reCAPTCHA',
    long_description="Python wrapper for Google reCAPTCHA",
    author='Javon Davis',
    author_email='javonldavis14@gmail.com, howarde.jr@hotmail.com, alexj.nich@hotmail.com',
    url='https://github.com/JunePlum/reCAPTCHA-Wrapper',
    license="MIT",
    packages=find_packages(exclude=('tests', 'docs'))
)
