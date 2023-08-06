
import glob
import sys
import os
from setuptools import setup, find_packages
from logtrails import __version__

setup(
    name = 'logtrails',
    keywords = 'logging redis pubsub message processor',
    description = 'Logging message queue processors',
    author = 'Ilkka Tuohela',
    author_email = 'hile@iki.fi',
    url = 'https://github.com/hile/logtrails/',
    version = __version__,
    license = 'PSF',
    packages = find_packages(),
    scripts = glob.glob('bin/*'),
    install_requires = (
        'systematic>=4.6.3',
        'multiprocess',
        'redis',
    ),
)

