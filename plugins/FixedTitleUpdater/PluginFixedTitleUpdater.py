from gio import File
import gc

name = "Fixed title updater plugin"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "FixedTitleUpdaterPlugin"
short_description = "Pretty python file names in window titler"
long_description = "Patches original TitleUpdater to show fully qualified python module names in window title"

def get_python_title(uri):
    f = File(uri)
    title = f.get_basename()
    packages = []
    while True:
        f = f.get_parent()
        if not f: break
        
        if f.get_child('__init__.py').query_exists():
            packages.append(f.get_basename())
        else:
            break
            
    if packages:
        if title != '__init__.py':
            packages.insert(0, title.partition('.py')[0])
            
        return '.'.join(reversed(packages))
    else:
        return title

class FixedTitleUpdaterPlugin(object):

    def __init__(self, editor):
        self.editor = editor

    def do_patch(self):
        from SCRIBES.GUI.MainGUI.Window.TitleUpdater import Updater

        if hasattr(Updater, '_patched_by_fixed_title_updater'):
            return

        def new_get_dictionary(this, uri):
            title = File(uri).get_basename() if uri else _("Unnamed Document")

            if title.endswith('.py'):
                title = get_python_title(uri)

            return {
                "normal": title,
                "modified": "*" + title,
                "readonly": title + _(" [READONLY]"),
                "loading": _("Loading %s ...") % title,
            }

        Updater._Updater__get_dictionary = new_get_dictionary
        Updater._patched_by_fixed_title_updater = True
        
        for r in gc.get_referrers(Updater):
            if isinstance(r, Updater):
                r._Updater__dictionary = new_get_dictionary(None, r._Updater__uri)
                
        self.editor.window.set_title(new_get_dictionary(None, self.editor.uri)['normal'])
        
    def load(self):
        self.do_patch()

    def unload(self):
        pass
