# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='dynamic_workflow',
    version='1.0.0',
    description='Advanced workflow engine for ERPNext with approval matrix, dynamic nodes, and WeChat integration',
    author='Your Company',
    author_email='your-email@example.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    python_requires='>=3.8',
)
