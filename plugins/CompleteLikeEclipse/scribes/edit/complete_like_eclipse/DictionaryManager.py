from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "updated-dictionary", self.__updated_dictionary_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__dictionary = {}
		return 

	def __destroy(self):
		self.disconnect()
		self.__dictionary.clear()
		del self.__dictionary
		del self
		return 

	def __update(self, dictionary):
		self.__dictionary.clear()
		self.__dictionary.update(dictionary)
		self.__manager.emit("dictionary", self.__dictionary)
		self.__manager.emit("finished-indexing")
		return False

	def __precompile_methods(self):
		methods = (self.__update, self.__updated_dictionary_cb,)
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __updated_dictionary_cb(self, manager, dictionary):
		from gobject import idle_add
		idle_add(self.__update, dictionary, priority=9999)
		return False
