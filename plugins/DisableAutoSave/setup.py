from setuptools import setup, find_packages
import os.path

def get_home():
    if 'SUDO_USER' in os.environ:
        return os.path.expanduser('~' + os.environ['SUDO_USER'])
    else:
        return os.path.expanduser('~')
        

setup(
    name     = 'scribes.edit.disable-auto-save',
    version  = '0.1',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Scribes plugin. Disables default autosave on timer and editor focus loss',
    long_description = open('README.rst').read(),
    zip_safe   = False,
    data_files = [
        (os.path.join(get_home(), '.gnome2', 'scribes', 'plugins'), ['PluginDisableAutoSave.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
