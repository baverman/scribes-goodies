from setuptools import setup, find_packages

setup(
    name     = 'scribes.edit.disable-auto-save',
    version  = '0.2.3',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Scribes plugin. Disables default autosave on timer and editor focus loss',
    long_description = open('README.rst').read(),
    zip_safe   = False,
    data_files = [
        ('scribes/plugins', ['PluginDisableAutoSave.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
