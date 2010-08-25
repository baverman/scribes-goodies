from copy import copy

from .. import Signals

class Updater(object):

    def __init__(self, manager):
        self.manager = manager
        self.view = manager.gui.get_object("TreeView")
        self.model = self.view.get_model()
        self.column1 = self.view.get_column(0)
        self.column2 = self.view.get_column(1)
        self.data = []
        
        self.manager.signals.connect_signals(self)
        
    @Signals.model_data
    def populate(self, sender, data):
        if not data: return False
        if self.data == data: return False
        
        self.data = copy(data)
        self.view.window.freeze_updates()
        self.view.set_model(None)
        self.model.clear()
        
        for name, path in data:
            self.model.append([name, path])
            
        self.column1.queue_resize()
        self.column2.queue_resize()
        self.view.set_model(self.model)
        self.view.window.thaw_updates()
        
        self.manager.signals.updated_model.emit()
        
        return False

    @Signals.lines(idle=False)
    def clear(self, *args):
        if not len(self.model): return False
        self.view.window.freeze_updates()
        self.view.set_model(None)
        self.model.clear()
        self.view.set_model(self.model)
        self.view.window.thaw_updates()
        return False
