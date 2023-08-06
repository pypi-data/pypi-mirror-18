#!/usr/bin/env python

import platform
import sys
import shutil
from os import path, makedirs
import urllib
from subprocess import Popen
from setuptools import setup, find_packages, Command


root = path.realpath(path.dirname(__file__))


class InitCommand(Command):
    user_options = []
    description = 'Install essential package to manager python'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # install pip - python package manager
        url = 'https://bootstrap.pypa.io/get-pip.py'
        tmp_dir = path.join(root, 'tmp')
        install_file = path.join(tmp_dir, 'install-pip.py')
        if not path.isdir(tmp_dir):
            makedirs(tmp_dir)
        urllib.urlretrieve(url, install_file)
        if Popen([sys.executable, install_file]).wait() != 0:
            sys.exit(1)

        # install virtualenv package
        cmd = ['pip', 'install', 'virtualenv']
        if platform.os.name == 'posix':
            cmd.insert(0, 'sudo')
        if Popen(cmd).wait() != 0:
            sys.exit(1)

        # create virtual environment
        venv_cmd = ['virtualenv', '-p', '/usr/bin/python3.4', 'venv']
        if Popen(venv_cmd).wait() != 0:
            sys.exit(1)


class DevCommand(Command):
    user_options = []
    description = 'Install packages for development'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # install develop packages
        dev_file = path.join(root, 'dev-requires.txt')
        if Popen(['pip', 'install', '-r', dev_file]).wait() != 0:
            sys.exit(1)

        # install runtime dependency packages
        if Popen(['pip', 'install', '-e', '.']).wait() != 0:
            sys.exit(1)


class CleanCommand(Command):
    user_options = []
    description = 'Clean all of build result'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree(path.join(root, '.cache'), True)
        shutil.rmtree(path.join(root, 'dist'), True)
        shutil.rmtree(path.join(root, 'build'), True)
        shutil.rmtree(path.join(root, 'dest'), True)
        shutil.rmtree(path.join(root, 'gwisp.egg-info'), True)
        shutil.rmtree(path.join(root, '.eggs'), True)
        shutil.rmtree(path.join(root, 'tmp'), True)
        shutil.rmtree(path.join(root, 'temp'), True)


class CleanVenvCommand(Command):
    user_options = []
    description = 'Clean virtual environment'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        venv_dir = path.join(root, 'venv')
        shutil.rmtree(venv_dir, True)


setup(
    name='gwisp',
    version='0.3.0',
    description='http programing interface of tracker storage',
    long_description='see more on home page',
    keywords='time tracker storage api',
    author='kevin leptons',
    author_email='kevin.leptons@gmail.com',
    url='https://github.com/kevin-leptons/gwisp',
    download_url='https://github.com/kevin-leptons/gwisp',
    install_requires=[
        'falcon==1.0.0', 'pymongo==3.3.0',
        'google-api-python-client==1.5.4', 'pyjwt==1.4.2',
        'click==6.6', 'jsonschema==2.5.1', 'waitress==1.0.0',
        'normalizr==0.1.9'
    ],
    packages=find_packages(exclude=['script', 'test']),
    entry_points={
        'console_scripts': [
            'gwisp=gwisp.cli:cli',
        ]
    },
    cmdclass={
        'init': InitCommand,
        'clean': CleanCommand,
        'cleanvenv': CleanVenvCommand,
        'dev': DevCommand,
    }
)
