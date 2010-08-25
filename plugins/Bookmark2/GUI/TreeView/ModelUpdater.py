from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "model-data", self.__data_cb)
		self.connect(manager, "lines", self.__lines_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		self.__model = self.__view.get_model()
		self.__column1 = self.__view.get_column(0)
		self.__column2 = self.__view.get_column(1)
		self.__data = []
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __populate(self, data):
		if not data: return False
		if self.__data == data: return False
		from copy import copy
		self.__data = copy(data)
		self.__editor.response()
		self.__view.window.freeze_updates()
		self.__view.set_model(None)
		self.__model.clear()
		for name, path in data:
			self.__editor.response()
			self.__model.append([name, path])
		self.__column1.queue_resize()
		self.__column2.queue_resize()
		self.__view.set_model(self.__model)
		self.__view.window.thaw_updates()
		self.__editor.response()
		self.__manager.emit("updated-model")
		return False

	def __clear(self):
		self.__editor.response()
		if not len(self.__model): return False
		self.__view.window.freeze_updates()
		self.__view.set_model(None)
		self.__model.clear()
		self.__view.set_model(self.__model)
		self.__view.window.thaw_updates()
		self.__editor.response()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __data_cb(self, manager, data):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__populate, data)
		return False

	def __lines_cb(self, manager, lines):
		if not lines: self.__clear()
		return False
