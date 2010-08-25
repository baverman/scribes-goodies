from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.connect(manager, "destroy", self.__destroy_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __set_properties(self):
		from gtk import TreeView, CellRendererToggle, TreeViewColumn
		from gtk import TREE_VIEW_COLUMN_AUTOSIZE, CellRendererText
		from gtk import SORT_DESCENDING, SELECTION_MULTIPLE
		from gtk import TREE_VIEW_COLUMN_FIXED
		view = self.__view
#		view.get_selection().set_mode(SELECTION_MULTIPLE)
		# Create column for line numbers.
		column = TreeViewColumn()
		view.append_column(column)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_spacing(12)
		renderer = CellRendererText()
		column.pack_start(renderer, True)
		column.set_attributes(renderer, text=0)
		column.set_resizable(True)
		column.set_reorderable(False)
		# Create column for line text.
		column = TreeViewColumn()
		view.append_column(column)
		column.set_sizing(TREE_VIEW_COLUMN_FIXED)
		renderer = CellRendererText()
		column.pack_start(renderer, True)
		column.set_attributes(renderer, text=1)
		column.set_resizable(False)
		column.set_spacing(12)
		column.set_fixed_width(250)
		column.set_reorderable(False)
		view.set_model(self.__create_model())
		view.realize()
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(int, str)
		return model

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
