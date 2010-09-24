from setuptools import setup, find_packages

setup(
    name     = 'scribes.edit.complete_like_eclipse',
    version  = '0.2.4',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    description = 'Eclipse like word completition',
    long_description = open('README.rst').read(),
    zip_safe   = False,
    install_requires = ['scribes.helpers>=0.5'],
    packages = find_packages(),
    namespace_packages = ['scribes'],
    data_files = [
        ('scribes/plugins', ['PluginCompleteLikeEclipse.py']),
    ],
    url = 'http://github.com/baverman/scribes-goodies',    
)
