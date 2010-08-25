from ..signals import Signals

from .TreeView import Manager as TreeViewManager
from .Window import Window

class Manager(object):

    def __init__(self, signals, editor):
        self.signals = signals
        self.editor = editor
        self.treeview = TreeViewManager(self)
        self.window = Window(self)
        
    @property
    def gui(self):
        try:
            return self.__gui
        except AttributeError:
            self.__gui = self.editor.get_gui_object(globals(), "GUI.glade")
            
        return self.__gui
