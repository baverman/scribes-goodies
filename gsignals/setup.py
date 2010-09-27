from setuptools import setup, find_packages

def run_tests():
    import unittest, sys, os.path, glob
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))
    return unittest.defaultTestLoader.loadTestsFromNames(
        map(lambda r: os.path.splitext(os.path.basename(r))[0], glob.glob('tests/test_*.py')))

setup(
    name     = 'gsignals',
    version  = '0.2.1',
    author   = 'Anton Bobrov',
    author_email = 'bobrov@vl.ru',
    packages     = find_packages(),
    description = 'Wrappers for gobject signals',
    #long_description = open('README.txt').read(),
    zip_safe   = False,
    test_suite = '__main__.run_tests',
    url = 'http://github.com/baverman/scribes-goodies',
)
