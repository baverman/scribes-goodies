indexer_dbus_service = "org.sourceforge.ScribesWordCompletionIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesWordCompletionIndexer"

class Monitor(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		self.__start_up_check()
		from SCRIBES.Globals import session_bus
		session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0='net.sourceforge.Scribes')
		from gobject import timeout_add
		timeout_add(60000, self.__check_instances, priority=9999)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __get_services(self):
		from SCRIBES.Globals import dbus_iface
		return dbus_iface.ListNames()

	def __start_up_check(self):
		services = self.__get_services()
		if not (indexer_dbus_service in services): return
		print "Ooops! Found another completion indexer, killing this one."
		self.__manager.quit()
		return

	def __check_instances(self):
		services = self.__get_services()
		if services.count(indexer_dbus_service) == 1: return True
		print "Ooops! Found another completion indexer, killing this one."
		self.__manager.quit()
		return True

	def __name_change_cb(self, *args):
		self.__manager.quit()
		return False
