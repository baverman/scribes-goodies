from SCRIBES.SignalConnectionManager import SignalManager

class Generator(SignalManager):

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
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __text_from(self, line):
		self.__editor.response()
		start = self.__editor.textbuffer.get_iter_at_line(line)
		end = self.__editor.forward_to_line_end(start.copy())
		return self.__editor.textbuffer.get_text(start, end).strip(" \t\r\n")

	def __generate(self, lines):
		self.__editor.response()
		data = [(line + 1, self.__text_from(line)) for line in lines]
		self.__manager.emit("model-data", tuple(data))
		self.__editor.response()
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __lines_cb(self, manager, lines):
		from gobject import idle_add
		idle_add(self.__generate, lines)
		return False
