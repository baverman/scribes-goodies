from scribes_helpers import connect_signals 
from signals import signals

class Marker(object):

    def __init__(self, editor):
        editor.response()
        self.editor = editor
        self.lines = []
        
        connect_signals(self)
        editor.response()

    @signals.toggle
    def toggle(self, sender):
        line = self.editor.cursor.get_line()
        
        if line in self.lines:
            signals.remove.emit(line)
        else:
            signals.add.emit(line)
            
        return False

    @signals.lines(idle=False)
    def lines_cb(self, sender, lines):
        self.lines = lines
        return False
