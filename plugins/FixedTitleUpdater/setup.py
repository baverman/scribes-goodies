from setuptools import setup, find_packages
import os.path

setup(
    name     = 'scribes.editor.title-updater-fix',
    version  = '0.2',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Scribes plugin. Showes pretty names for python modules in editor titlebar',
    long_description = open('README.rst').read(),
    zip_safe   = False,
    data_files = [
        ('scribes/plugins', ['PluginFixedTitleUpdater.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
