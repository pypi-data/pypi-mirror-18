from setuptools import setup, find_packages
from codecs import open
from os import path

short_description = "Count Down Timer Application"

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    version = f.read()

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requires = f.readlines()

setup(
    name='CountDownApp',
    version=version,
    description=short_description,
    long_description=long_description,
    url='https://github.com/Himenon/CountDownApp',
    author='K.Himeno',
    author_email='k.himeno314@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment'
    ],
    keywords='timer',
    install_requires=requires,
)