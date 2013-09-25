from setuptools import setup, find_packages
import os
import os.path
import glib

def get_plugin_directory():
    if os.getuid() == 0:
        return x
    
# print("setuptools = dir %s" % dir(setuptools))

setup(
    name     = 'scribes.python.rope',
    version  = '0.3.4',
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
        (('%s/scribes/LanguagePlugins' % glib.get_user_config_dir()),
            ['PluginPythonRope.py']
        )
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
