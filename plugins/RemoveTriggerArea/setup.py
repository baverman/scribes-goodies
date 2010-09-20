from setuptools import setup, find_packages
import os.path

def get_home():
    if 'SUDO_USER' in os.environ:
        return os.path.expanduser('~' + os.environ['SUDO_USER'])
    else:
        return os.path.expanduser('~')
        

setup(
    name     = 'scribes.editor.remove-trigger-area',
    version  = '0.1',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Removes trigger area from scribes editor',
    long_description = open('README.rst').read(),
    zip_safe   = False,
    install_requires = ['scribes.helpers>=0.5'],
    data_files = [
        (os.path.join(get_home(), '.gnome2', 'scribes', 'plugins'), ['PluginRemoveTriggerArea.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
