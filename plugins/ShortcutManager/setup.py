from setuptools import setup, find_packages
import os.path

setup(
    name     = 'scribes.editor.shortcut-manager',
    version  = '0.2.3',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Shortcut manager for scribes editor',
    long_description = open('README.rst').read(),
    zip_safe   = False,
    install_requires = ['scribes.helpers>=0.5'],
    packages = find_packages(),
    include_package_data = True,
    namespace_packages = ['scribes'],
    data_files = [
        ('scribes/plugins', ['PluginShortcutManager.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
