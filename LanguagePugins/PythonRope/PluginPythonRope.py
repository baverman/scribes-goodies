name = "Python rope autocomplete"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
languages = ["python"]
version = 0.1
autoload = True
class_name = "PythonRopePlugin"
short_description = "Autocompletes python code"
long_description = """This plugin uses rope refactoring library
to autocomlete python code"""

from scribes_helpers import bootstrap

PythonRopePlugin = bootstrap('PythonRopeScribesPlugin.Plugin')
