from SCRIBES.SignalConnectionManager import SignalManager

class Window(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "show", self.__show_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "scroll-to-line", self.__delete_event_cb)
		self.connect(self.__window, "delete-event", self.__delete_event_cb)
		self.connect(self.__window, "key-press-event", self.__key_press_event_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__window = manager.gui.get_object("Window")
		return False

	def __set_properties(self):
		self.__window.set_transient_for(self.__editor.window)
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __hide(self):
		self.__editor.response()
		self.__window.hide()
		self.__editor.response()
		return False

	def __show(self):
		self.__editor.response()
		self.__window.show_all()
		self.__editor.response()
		return False

	def __delete_event_cb(self, *args):
		self.__manager.emit("hide")
		return True

	def __key_press_event_cb(self, window, event):
		from gtk.keysyms import Escape
		if event.keyval != Escape: return False
		self.__manager.emit("hide")
		return True

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show)
		return False

	def __hide_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__hide)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
