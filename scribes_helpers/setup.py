from setuptools import setup, find_packages

def run_tests():
    import unittest, os.path, sys
    unittest.defaultTestLoader
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    import test_plugin_gc
    return unittest.defaultTestLoader.loadTestsFromModule(test_plugin_gc)

setup(
    name     = 'scribes.helpers',
    version  = '0.2dev',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    package_dir  = {'':'src'},    
    packages     = ['scribes_helpers'],
    description = 'Wrappers for easy scribes plugins development',
    long_description = open('README.txt').read(),
    zip_safe   = False,
    test_suite = '__main__.run_tests',
    url = 'http://github.com/baverman/scribes-goodies',
)
