#!/usr/bin/env python

'''
    Execution:
        python setup.py build
        python setup.py install
    Purpose:
        This is the setup script for the app
'''

__author__ = 'Matt Joyce'
__email__ = 'matt@nycresistor.com'
__copyright__ = 'Copyright 2016, Symphony Communication Services LLC'

from setuptools import setup, find_packages
from pip.req import parse_requirements


# parse_requirements() returns generator of
# pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt',
                                  session=False)

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='metronome',
    version='0.0.15',
    description='metronome diagnostics bot',
    author='Matt Joyce',
    author_email='matt@nycresistor.com',
    url='https://github.com/symphonyoss/metronome',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='symphony chat diagnostics',
    # install dependencies from requirements.txt
    install_requires=reqs,
    packages=find_packages(),
    # bin files / python standalone executable scripts
    scripts=['bin/metronome.py'],
    include_package_data=True,
    zip_safe=False,
)
