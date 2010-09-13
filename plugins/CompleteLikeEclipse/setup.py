from setuptools import setup, find_packages
import os.path

def get_home():
    if 'SUDO_USER' in os.environ:
        return os.path.expanduser('~' + os.environ['SUDO_USER'])
    else:
        return os.path.expanduser('~')
        

setup(
    name     = 'scribes.edit.complete_like_eclipse',
    version  = '0.2.2',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Eclipse like word completition',
    zip_safe   = False,
    install_requires = ['scribes.helpers>=0.5'],
    packages = find_packages(),
    namespace_packages = ['scribes'],
    data_files = [
        (os.path.join(get_home(), '.gnome2', 'scribes', 'plugins'), ['PluginCompleteLikeEclipse.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
