from dbus.service import Object, method, BusName, signal

indexer_dbus_service = "org.sourceforge.ScribesWordCompletionIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesWordCompletionIndexer"

class DBusService(Object):

	def __init__(self, manager):
		from SCRIBES.Globals import session_bus
		bus_name = BusName(indexer_dbus_service, bus=session_bus)
		Object.__init__(self, bus_name, indexer_dbus_path)
		self.__manager = manager
		manager.connect("finished", self.__finished_cb)

	@method(indexer_dbus_service, in_signature="sx")
	def process(self, text, id_):
		return self.__manager.process(text, id_)

	@signal(indexer_dbus_service, signature="xa{sx}")
	def finished(self, id_, dictionary):
		return # return

	def __finished_cb(self, manager, data):
		editor_id, dictionary = data
		self.finished(editor_id, dictionary)
		return False
