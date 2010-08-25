from scribes_helpers import Plugin, Signal, SignalManager, Trigger
from gettext import gettext as _

name = "Bar Plugin"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "BarPlugin"
short_description = "Unleashes Bar's awesome powers!"
long_description = """Example plugin to show how to design plugins"""


class Signals(SignalManager):
    show_message = Signal(1)
    show_info = Signal(2)


trigger = Trigger("activate-bar-power", "<ctrl><alt>f", 
    _("Activate the holy power of bar"), _("Example"))


class BarPlugin(Plugin):
    def __init__(self, editor):
        super(BarPlugin, self).__init__(editor)
        self.signals = Signals()
        self.signals.connect_signals(self)
        
    @trigger
    def activate(self, sender):
        message = "Witness the awesome power of Bar!"
        title = "Real Bar Power"
        
        self.signals.show_message.emit(message)
        self.signals.show_info.emit(title, message)
        return False

    @Signals.show_message    
    def show_message(self, sender, message):
        # Update the message bar.
        self.editor.update_message(message, "yes", 10)
        return False

    @Signals.show_info(idle=False, after=True)
    def show_info(self, sender, title, message):      
        # Show a window containing Bar message.
        self.editor.show_info(title, message, self.editor.window)
        return False
