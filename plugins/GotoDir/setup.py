from setuptools import setup, find_packages
import os.path

setup(
    name     = 'scribes.file.goto-dir',
    version  = '0.2',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Scribes plugin. Opens current file directory in file manager',
    long_description = open('README.rst').read(),
    zip_safe   = False,
    install_requires = ['scribes.helpers>=0.3dev'],
    data_files = [
        ('scribes/plugins', ['PluginGotoDir.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
