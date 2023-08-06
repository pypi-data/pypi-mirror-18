import sys
import codecs
import uuid
from random import randint as r
from setuptools import setup

def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


setup(
    name='readme-test',
    version='{}.{}.{}'.format(r(0,9), r(0,9), r(0,9)),
    description='testing readme rendering on pypi',
    long_description=long_description(),
    url='http://httpie.org/',
    download_url='https://github.com/jkbrzt/httpie',
    author_email='jakub@roztocil.co',
    license='bsd',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
)
