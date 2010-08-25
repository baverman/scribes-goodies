from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "Bookmark", "Bookmark.gdb")

def get_value(uri):
	try:
		database = open_database(basepath, "r")
		lines = database[uri] if database.has_key(uri) else ()
	except:
		pass
	finally:
		database.close()
	return lines

def set_value(uri, lines):
	try:
		database = open_database(basepath, "w")
		if lines: database[uri] = lines
		if not lines and database.has_key(uri): del database[uri]
	finally:
		database.close()
	return
