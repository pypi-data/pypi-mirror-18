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
)
