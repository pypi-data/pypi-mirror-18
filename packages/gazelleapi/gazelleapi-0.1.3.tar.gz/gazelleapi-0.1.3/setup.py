"""
Installer file for our lovely api
"""

from setuptools import setup, find_packages
from gazelleapi import __version__, __author__, __author_email__, __url__, __description__

setup(
    name='gazelleapi',
    version=__version__,
    description='Gazelle API',
    long_description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license='MIT',
    install_requires=[
        "future",
        "requests"
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={
        '': ['*.txt']
    },
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ]
)
