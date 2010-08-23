import time
import os
from gio import File

name = "Fixed Quick Open plugin"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "FixedQuickOpenPlugin"
short_description = "Keep start directory from changing"
long_description = "Patches original QuickOpen for emmiting only start directory"

import quick_open_settings as settings

class FixedQuickOpenPlugin(object):

    def __init__(self, editor):
        editor.response()
        self.editor = editor
        self.last_root = None

    def load(self):
        from QuickOpen.FolderPathUpdater import Updater

        def new_updater(this, parent=False):
            editor_uri = this._Updater__editor.pwd_uri
            print editor_uri
            
            root = None
            for p in settings.recent_pathes:
                if editor_uri.startswith(p):
                    root = p
                    break

            if not root:
                root = self.find_project_root(editor_uri)
                settings.recent_pathes.append(root)

            
            if parent:
                i = settings.recent_pathes.index(self.last_root or root)
                root = settings.recent_pathes[(i + 1) % len(settings.recent_pathes)]
                self.last_root = root

            this._Updater__manager.emit("current-path", root)

            return False

        Updater._Updater__update = new_updater


    def unload(self):
        pass

    def find_project_root(self, path):
        f = File(path)
        while True:
            if f.get_child('.scribes_project').query_exists():
                return f.get_uri()

            p = f.get_parent()
            if p:
                f = p
            else:
                return path

