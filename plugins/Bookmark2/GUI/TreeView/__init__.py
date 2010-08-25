from gtk import TreeView, CellRendererToggle, TreeViewColumn
from gtk import TREE_VIEW_COLUMN_AUTOSIZE, CellRendererText
from gtk import SORT_DESCENDING, SELECTION_MULTIPLE
from gtk import TREE_VIEW_COLUMN_FIXED
from gtk import ListStore

from scribes_helpers import weak_connect

from .. import Signals

from ModelUpdater import Updater


class Manager(object):

    def __init__(self, manager):
        self.manager = manager
        self.view = manager.gui.get_object("TreeView")
        
        self.manager.signals.connect_signals(self)
        weak_connect(self.view, "row-activated", self, 'row_activated')

        self.set_properties()
        
        self.updater = Updater(manager)

    def set_properties(self):
        view = self.view
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
        view.set_model(self.create_model())
        view.realize()

    def create_model(self):
        return ListStore(int, str)
    
    @Signals.lines
    def sensitive(self, sender, lines):
        self.view.set_property("sensitive", bool(lines))
        return False
    
    @Signals.show
    def select_first_row(self, sender):
        if not len(self.view.get_model()):
            return False
        self.view.get_selection().select_path(0)
        self.view.set_cursor(0, self.view.get_column(0))
        self.view.scroll_to_cell(0, None, True, 0.5, 0.5)
        return False
    
    def row_activated(self, *args):
        selection = self.view.get_selection()
        model, iterator = selection.get_selected()
        line = model.get_value(iterator, 0) - 1
        self.manager.signals.scroll_to_line.emit(line)
        return False
    
    def text_from(self, line):
        start = self.manager.editor.textbuffer.get_iter_at_line(line)
        end = self.manager.editor.forward_to_line_end(start.copy())
        return self.manager.editor.textbuffer.get_text(start, end).strip(" \t\r\n")

    @Signals.lines
    def generate(self, sender, lines):
        data = [(line + 1, self.text_from(line)) for line in lines]
        self.manager.signals.model_data.emit(tuple(data))
        return False
