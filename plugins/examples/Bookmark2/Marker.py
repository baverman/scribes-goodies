from .signals import Signals

class Marker(object):

    def __init__(self, signals, editor):
        self.editor = editor
        self.signals = signals        
        self.lines = []
        
        self.signals.connect_signals(self)

    @Signals.toggle
    def toggle(self, sender):
        line = self.editor.cursor.get_line()
        
        if line in self.lines:
            self.signals.remove.emit(line, True)
        else:
            self.signals.add.emit(line, True)
            
        return False

    @Signals.lines(idle=False)
    def lines_cb(self, sender, lines):
        self.lines = lines
        return False
