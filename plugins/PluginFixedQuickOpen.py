import time

name = "Fixed Quick Open plugin"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "FixedQuickOpenPlugin"
short_description = "Keep start directory from changing"
long_description = "Patches original QuickOpen for emmiting only start directory"

class FixedQuickOpenPlugin(object):

    def __init__(self, editor):
        editor.response()
        self.editor = editor
		
    def load(self):
        # Try to import Updater class
        for i in range(10):
            try:
                from QuickOpen.FolderPathUpdater import Updater
                break
            except ImportError:
                self.editor.response()
                time.sleep(0.5)
                
        if i > 9:
            print "Can't import QuickOpen.FolderPathUpdater.Updater"
            return

        import os
        from gio import File

        path = File(os.curdir).get_uri()

        old_updater = Updater._Updater__update

        def new_updater(this, parent=False):
            this._Updater__manager.emit("current-path", path)
            return False

        Updater._Updater__update = new_updater


    def unload(self):
        pass
