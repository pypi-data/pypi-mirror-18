from setuptools import setup
from sys import version_info as py_version
from textwrap import dedent

VERSION = '0.0.2'

REQUIREMENTS = ['wrapt>=1.10.8']
MODULES = []

if py_version < (3, 5):
    REQUIREMENTS.append('typing')

setup(
    name='carl',
    version=VERSION,
    py_modules=['carl'],
    install_requires=REQUIREMENTS,
    url='https://gitlab.com/tarcisioe/carl',
    download_url=('https://gitlab.com/tarcisioe/carl/repository/'
                  'archive.tar.gz?ref=' + VERSION),
    keywords=['entry', 'points', 'subcommands'],
    maintainer='Tarcísio Eduardo Moreira Crocomo',
    maintainer_email='tarcisio.crocomo+pypi@gmail.com',
    description=dedent('''\
        An entry-point library based on argparse, to make creating cli tools
        as easy as possible.
        '''),
)
