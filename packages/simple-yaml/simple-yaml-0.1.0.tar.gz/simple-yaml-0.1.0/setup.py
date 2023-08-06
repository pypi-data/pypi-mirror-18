# coding:utf-8
"""
Simple YAML

Document: https://github.com/guyskk/simple-yaml
"""
from setuptools import setup

setup(
    name="simple-yaml",
    version="0.1.0",
    description="A simple version of pyyaml",
    long_description=__doc__,
    author="guyskk",
    author_email='guyskk@qq.com',
    url="https://github.com/guyskk/simple-yaml",
    license="MIT",
    py_modules=["simple_yaml"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyyaml>=3.11'
    ],
    keywords='sample yaml pyyaml',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
