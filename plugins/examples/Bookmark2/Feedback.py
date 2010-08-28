from gettext import gettext as _

from .signals import Signals

MESSAGE = _("Bookmarked lines")

class Feedback(object):
    def __init__(self, signals, editor):
        self.editor = editor
        signals.connect_signals(self)

    @Signals.add(after=True)
    def add(self, sender, line, feedback=None):
        if feedback:
            message = _("Marked line %d") % (line + 1)
            self.editor.update_message(message, "yes")
            
        return False

    @Signals.remove(after=True)
    def remove(self, sender, line, feedback=None):
        if feedback:
            message = _("Unmarked line %d") % (line + 1)
            self.editor.update_message(message, "yes")
        return False

    @Signals.remove_all
    def remove_all(self, sender, feedback=None):
        if feedback:
            message = _("Removed all bookmarks")
            self.editor.update_message(message, "yes")

        return False

    @Signals.show(idle=False)
    def show(self, *args):
        self.editor.set_message(MESSAGE)
        return False

    @Signals.hide(idle=False)
    def hide(self, *args):
        self.editor.unset_message(MESSAGE)
        return False

    @Signals.scroll_to_line(idle=False)
    def scroll_to_line(self, manager, line):
        message = _("Cursor on line %d") % (line + 1)
        self.editor.update_message(message, "yes")
        return False
