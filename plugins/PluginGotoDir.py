from scribes.helpers import Trigger, TriggerManager
import subprocess
from gettext import gettext as _

name = "GotoDir Plugin"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "GotoDirPlugin"
short_description = "Opens file directory"
long_description = "Opens file directory in thunar file manager"


trigger = Trigger("open-file-directory", "<ctrl><alt>l", 
    _("Opens file directory in file manager"), _("File Operations"))


class GotoDirPlugin(object):
    def __init__(self, editor):
        self.editor = editor
        self.triggers = TriggerManager(editor)
        self.triggers.connect_triggers(self)
    
    @trigger
    def activate(self, sender):
        subprocess.Popen(['/usr/bin/env', 'xdg-open', self.editor.pwd_uri]).poll()
        return False
    
    def load(self): pass
    def unload(self): pass
