from setuptools import setup, find_packages
import os.path

setup(
    name     = 'scribes.python.rope',
    version  = '0.3.3',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Scribes plugin. Python code autocompleter',
    long_description = open('README.txt').read(),
    zip_safe   = False,
    install_requires = ['scribes.helpers>=0.5', 'rope>=0.9'],
    packages = find_packages(),
    include_package_data = True,
    namespace_packages = ['scribes'],
    data_files = [
        ('scribes/LanguagePlugins', ['PluginPythonRope.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
