from scribes_helpers import Plugin, Signal, SignalManager, Trigger
import subprocess

name = "GotoDir Plugin"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "GotoDirPlugin"
short_description = "Opens file directory"
long_description = "Opens file directory in thunar file manager"


trigger = Trigger("activate-goto-dir", "<ctrl><alt>l", 
    _("Opens file directory in file manage"), _("Open dir"))


class GotoDirPlugin(Plugin):
    
    @trigger
    def activate(self, sender):
        subprocess.Popen(['/usr/bin/env', 'thunar', self.editor.pwd_uri]).poll()
        return False
