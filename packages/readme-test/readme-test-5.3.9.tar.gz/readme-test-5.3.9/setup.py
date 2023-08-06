import codecs
from random import randint
from setuptools import setup

def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()

def random_version():
    return '{}.{}.{}'.format(randint(0, 9), randint(0, 9), randint(0, 9))

setup(
    name='readme-test',
    version=random_version(),
    description='testing readme rendering on pypi',
    long_description=long_description(),
    url='http://httpie.org/',
    download_url='https://github.com/jkbrzt/httpie',
    author_email='jakub@roztocil.co',
    license='bsd',
)
