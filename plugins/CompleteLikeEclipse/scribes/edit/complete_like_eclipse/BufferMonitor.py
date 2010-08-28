class Monitor(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__buffer.connect("changed", self.__changed_cb)
		self.__sigid3 = manager.connect("finished-indexing", self.__finished_indexing_cb)
		self.__sigid4 = editor.connect("loaded-file", self.__changed_cb)
		self.__sigid5 = editor.connect("renamed-file", self.__changed_cb)
		self.__sigid6 = manager.connect("found-indexer-process", self.__changed_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__is_busy = False
		self.__changed = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		del self
		self = None
		return False

	def __start_indexing_async(self):
		if self.__is_busy: return False
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(500, self.__start_indexing, priority=9999)
			self.__changed = False
		return False

	def __start_indexing(self):
		self.__manager.emit("start-indexing")
		self.__is_busy = True
		return False

	def __precompile_methods(self):
		methods = (self.__changed_cb, self.__start_indexing_async,
			self.__start_indexing,)
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		self.__changed = True
		self.__start_indexing_async()
		return False

	def __finished_indexing_cb(self, *args):
		self.__is_busy = False
		if self.__changed: self.__start_indexing_async()
		return False
