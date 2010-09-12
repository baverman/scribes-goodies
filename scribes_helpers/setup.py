from setuptools import setup, find_packages

setup(
    name     = 'scribes.helpers',
    version  = '0.4',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    packages     = find_packages(),
    description = 'Wrappers for easy scribes plugins development',
    long_description = open('README.txt').read(),
    install_requires = ['gsignals>=0.1'],
    zip_safe   = False,
    url = 'http://github.com/baverman/scribes-goodies',
    namespace_packages = ['scribes'],
)
