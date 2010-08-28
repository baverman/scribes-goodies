indexer_dbus_service = "org.sourceforge.ScribesWordCompletionIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesWordCompletionIndexer"

class Communicator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("extracted-text", self.__extract_text_cb)
		editor.session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=indexer_dbus_service)
		editor.session_bus.add_signal_receiver(self.__finished_cb,
						signal_name="finished",
						dbus_interface=indexer_dbus_service)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__indexer = self.__get_indexer()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.session_bus.remove_signal_receiver(self.__name_change_cb,
			'NameOwnerChanged',
			'org.freedesktop.DBus',
			'org.freedesktop.DBus',
			'/org/freedesktop/DBus',
			arg0=indexer_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(self.__finished_cb,
			signal_name="finished",
			dbus_interface=indexer_dbus_service)
		del self
		self = None
		return False

	def __get_indexer(self):
		from SCRIBES.Globals import dbus_iface, session_bus, python_path
		services = dbus_iface.ListNames()
		if not (indexer_dbus_service in services): return None
		indexer = session_bus.get_object(indexer_dbus_service, indexer_dbus_path)
		self.__manager.emit("found-indexer-process")
		return indexer

	def __send_text(self, text):
		try:
			self.__indexer.process(text.decode("utf8"), self.__editor.id_,
				dbus_interface=indexer_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		except AttributeError:
			print "ERROR:No word completion indexer process found"
			self.__indexer = self.__get_indexer()
			if self.__indexer is None: self.__manager.emit("finished-indexing")
		except:
			print "ERROR: Cannot send message to word completion indexer"
			self.__manager.emit("finished-indexing")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __extract_text_cb(self, manager, text):
		from gobject import idle_add
		idle_add(self.__send_text, text)
		return False

	def __name_change_cb(self, *args):
		self.__indexer = self.__get_indexer()
		return False

	def __finished_cb(self, editor_id, dictionary):
		if editor_id != self.__editor.id_: return False
		self.__manager.emit("updated-dictionary", dictionary)
		return False

	def __reply_handler_cb(self, *args):
		return False

	def __error_handler_cb(self, *args):
		print "ERROR: Failed to communicate with word completion indexer"
		self.__manager.emit("finished-indexing")
		return False
