from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(self.__view, "row-activated", self.__activated_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		self.__selection = self.__view.get_selection()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __activate(self):
		selection = self.__view.get_selection()
		model, iterator = selection.get_selected()
		line = model.get_value(iterator, 0) - 1
		self.__manager.emit("scroll-to-line", line)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return True
