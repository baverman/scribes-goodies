from setuptools import setup, find_packages
import os.path

setup(
    name     = 'scribes.editor.remove-trigger-area',
    version  = '0.2',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Removes trigger area from scribes editor',
    long_description = open('README.rst').read(),
    zip_safe   = False,
    install_requires = ['scribes.helpers>=0.5'],
    data_files = [
        ('scribes/plugins', ['PluginRemoveTriggerArea.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
