indexer_dbus_service = "org.sourceforge.ScribesWordCompletionIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesWordCompletionIndexer"

class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		editor.session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=indexer_dbus_service)
		from gobject import timeout_add
		timeout_add(2000, self.__start, priority=99999)
		editor.response()

	def __init_attributes(self, manager, editor):
		from os.path import join, split
		from sys import prefix
		self.__manager = manager
		self.__editor = editor
		self.__cwd = self.__editor.get_current_folder(globals())
		exec_folder = join(self.__cwd, "IndexerProcess")
		self.__executable = join(exec_folder, "ScribesWordCompletionIndexer.py")
		self.__python_executable = join(prefix, "bin", "python")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.session_bus.remove_signal_receiver(self.__name_change_cb,
			'NameOwnerChanged',
			'org.freedesktop.DBus',
			'org.freedesktop.DBus',
			'/org/freedesktop/DBus',
			arg0=indexer_dbus_service)
		del self
		self = None
		return False

	def __start(self):
		from gobject import idle_add
		idle_add(self.__start_process, priority=99999)
		return False

	def __start_process(self):
		if self.__indexer_process_exists(): return False
		self.__start_indexer_process()
		return False

	def __indexer_process_exists(self):
		services = self.__editor.dbus_iface.ListNames()
		if indexer_dbus_service in services: return True
		return False

	def __start_indexer_process(self):
		try:
			from gobject import spawn_async
			spawn_async([self.__python_executable, self.__executable,
			self.__editor.python_path], working_directory=self.__cwd)
		except:
			pass
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __name_change_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__start_process)
		return False
