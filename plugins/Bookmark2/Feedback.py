from gettext import gettext as _
from scribes_helpers import connect_signals 

from signals import signals

MESSAGE = _("Bookmarked lines")

class Feedback(object):
    def __init__(self,  editor):
        self.feedback = None
        self.editor = editor
        
        connect_signals(self)

    @signals.add(after=True)
    def add(self, sender, line):
        if not self.feedback: return False
        message = _("Marked line %d") % (line + 1)
        self.editor.update_message(message, "yes")
        return False

    @signals.remove(after=True)
    def remove(self, sender, line):
        if not self.feedback: return False
        message = _("Unmarked line %d") % (line + 1)
        self.editor.update_message(message, "yes")
        return False

    @signals.remove_all
    def remove_all(self, sender):
        if not self.feedback: return False
        message = _("Removed all bookmarks")
        self.editor.update_message(message, "yes")
        return False

    @signals.feedback
    def feedback(self, sender, feedback):
        self.feedback = feedback
        return False

    @signals.show
    def show(self, *args):
        self.editor.set_message(MESSAGE)
        return False

    @signals.hide
    def hide(self, *args):
        self.editor.unset_message(MESSAGE)
        return False

    @signals.scroll_to_line
    def scroll_to_line(self, manager, line):
        message = _("Cursor on line %d") % (line + 1)
        self.editor.update_message(message, "yes")
        return False
