from scribes_helpers import Plugin, Signal, SignalManager, Trigger
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


class GotoDirPlugin(Plugin):
    
    @trigger
    def activate(self, sender):
        subprocess.Popen(['/usr/bin/env', 'thunar', self.editor.pwd_uri]).poll()
        return False
