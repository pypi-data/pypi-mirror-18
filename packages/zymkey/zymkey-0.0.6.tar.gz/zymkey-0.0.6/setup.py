#!/usr/bin/env python
import os

from distutils.core import setup

SCRIPT_DIR = os.path.dirname(__file__)
if not SCRIPT_DIR:
        SCRIPT_DIR = os.getcwd()

# put together list of requirements to install
install_requires = []
REQUIREMENTS = os.path.join(SCRIPT_DIR, 'requirements.txt')
if os.path.exists(REQUIREMENTS):
    with open(REQUIREMENTS) as fh:
        for line in fh.readlines():
            if line.startswith('-'):
                continue

            install_requires.append(line.strip())

long_description = ''
README = os.path.join(SCRIPT_DIR, 'README.md')
if os.path.exists(README):
    long_description = open(README, 'r').read()



def get_files(path):
    """
    path: relative to SCRIPT_DIR
    """
    full_path = os.path.join(SCRIPT_DIR, path)
    return [os.path.join(path, x) for x in os.listdir(full_path)]


data_files = [
    ('/usr/local/lib', ['lib/libzk_app_utils.so']),
    ('share/zymkey/exmaples', get_files('examples')),
]

setup(name='zymkey',
      version='0.0.6',
      description='Zymkey utilities',
      author='Zymbit, Inc.',
      author_email='code@zymbit.com',
      packages=[
          'zymkey',
      ],
      data_files=data_files,
      long_description=long_description,
      url='https://zymbit.com/',
      license='LICENSE',
      install_requires=install_requires,
)
