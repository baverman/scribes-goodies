from setuptools import setup, find_packages
import os.path

setup(
    name     = 'scribes.file.quick-open-fix',
    version  = '0.2.3',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Scribes plugin. Adds project support to stock quick open plugin',
    zip_safe   = False,
    data_files = [
        ('scribes/plugins', ['PluginFixedQuickOpen.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
