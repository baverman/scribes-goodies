from setuptools import setup
import os.path

def get_home():
    if 'SUDO_USER' in os.environ:
        return os.path.expanduser('~' + os.environ['SUDO_USER'])
    else:
        return os.path.expanduser('~')
        

setup(
    name     = 'scribes.python.rope',
    version  = '0.1dev',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Python code autocomplete for scribes editor',
    long_description = open('README.txt').read(),
    zip_safe   = False,
    install_requires = ['scribes.helpers>=0.2dev'],
    packages = ['PythonRopeScribesPlugin'],
    data_files = [
        (os.path.join(get_home(), '.gnome2', 'scribes', 'LanguagePlugins'), ['PluginPythonRope.py']),
    ],
    include_package_data = True,
    url = 'http://github.com/baverman/scribes-goodies'
)
