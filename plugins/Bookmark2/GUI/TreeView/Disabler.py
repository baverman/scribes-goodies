from SCRIBES.SignalConnectionManager import SignalManager

class Disabler(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "lines", self.__lines_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __sensitive(self, files):
		value = True if files else False
		self.__editor.response()
		self.__view.set_property("sensitive", value)
		self.__editor.response()
		return False

	def __lines_cb(self, manager, lines):
		from gobject import idle_add
		idle_add(self.__sensitive, lines)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
