from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION, TYPE_STRING
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"new-job": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"finished": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"generate-dictionary": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
		from IndexerProcessMonitor import Monitor
		Monitor(self)
		from DBusService import DBusService
		DBusService(self)
		from DictionaryGenerator import Generator
		Generator(self)
		from JobSpooler import Spooler
		Spooler(self)

	def quit(self):
		from os import _exit
		_exit(0)
		return

	def process(self, text, editor_id):
		self.emit("new-job", (text, editor_id))
		return False
