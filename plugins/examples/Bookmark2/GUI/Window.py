from gtk.keysyms import Escape

from scribes_helpers import weak_connect

from ..signals import Signals 

class Window(object):

    def __init__(self, manager):
        self.manager = manager
        self.window = manager.gui.get_object("Window")
        self.window.set_transient_for(manager.editor.window)
        
        manager.signals.connect_signals(self)
        weak_connect(self.window, "delete-event", self, 'delete_event', idle=False)
        weak_connect(self.window, "key-press-event", self, 'key_press_event', idle=False)

    @Signals.hide
    def hide(self, sender):
        self.window.hide()
        return False

    @Signals.show
    def show(self, sender):
        self.window.show_all()
        return False

    @Signals.scroll_to_line(idle=False)
    def delete_event(self, *args):
        self.manager.signals.hide.emit()
        return True

    def key_press_event(self, window, event):
        if event.keyval != Escape:
            return False
    
        self.manager.signals.hide.emit()
        
        return True
