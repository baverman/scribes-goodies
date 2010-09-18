from scribes.helpers import Trigger, TriggerManager
import subprocess
from gettext import gettext as _

name = "Remove trigger area plugin"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "TriggerAreaPlugin"
short_description = "Removes trigger area"
long_description = "Removes trigger area"


trigger = Trigger("show-full-view", "<ctrl><alt>m", 
    _("Show editor's fullview"), _("Miscellaneous Operations"))


class TriggerAreaPlugin(object):
    def __init__(self, editor):
        self.editor = editor
        self.triggers = TriggerManager(editor)
        self.triggers.connect_triggers(self)
    
    @trigger
    def activate(self, sender):
        self.editor.show_full_view()
        return False
    
    def load(self): pass
    def unload(self): pass
