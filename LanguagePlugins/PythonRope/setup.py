from setuptools import setup, find_packages
import os.path

def get_home():
    if 'SUDO_USER' in os.environ:
        return os.path.expanduser('~' + os.environ['SUDO_USER'])
    else:
        return os.path.expanduser('~')
        

setup(
    name     = 'scribes.python.rope',
    version  = '0.3.2',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Scribes plugin. Python code autocompleter',
    long_description = open('README.txt').read(),
    zip_safe   = False,
    install_requires = ['scribes.helpers>=0.5'],
    packages = find_packages(),
    include_package_data = True,
    namespace_packages = ['scribes'],
    data_files = [
        (os.path.join(get_home(), '.gnome2', 'scribes', 'LanguagePlugins'), ['PluginPythonRope.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
