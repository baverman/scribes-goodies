name = "Disable auto save plugin"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "DisableAutoSavePlugin"
short_description = "Turns off autosave feature"
long_description = "Patches AutomaticSaver and FocusOutSaver"


class DisableAutoSavePlugin(object):

    def __init__(self, editor):
        pass

    def patch_auto_saver(self):
        try:
            from SCRIBES.SaveSystem.AutomaticSaver import Saver
        except ImportError:
            print "Can't find autosaver class"

        def remove_timer(this, *args):
            Saver._Saver__remove_timer(this)
            return False
                
        Saver._Saver__process = remove_timer 
        Saver._Saver__save_on_idle = remove_timer
        Saver._Saver__save = remove_timer
        
    def patch_focusout_saver(self):
        try:
            from SCRIBES.SaveSystem.FocusOutSaver import Saver
        except ImportError:
            print "Can't find focus out saver class"

        Saver._Saver__save = lambda *args: False

    def load(self):
        self.patch_auto_saver()
        self.patch_focusout_saver()

    def unload(self):
        pass
