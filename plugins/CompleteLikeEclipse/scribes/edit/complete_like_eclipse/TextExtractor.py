class Extractor(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("start-indexing", self.__start_indexing_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __extract_text(self):
		texts = []
		for editor in self.__editor.instances:
			self.__editor.response()
			texts.append(editor.text)
		text = " ".join(texts)
		self.__manager.emit("extracted-text", text)
		return False

	def __precompile_methods(self):
		methods = (self.__extract_text, )
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __start_indexing_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__extract_text, priority=9999)
		return False
