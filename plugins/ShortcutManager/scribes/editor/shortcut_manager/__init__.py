import gc
import os.path

from gtk import accel_groups_from_object, accelerator_parse, accelerator_name
from gtk import ACCEL_LOCKED, STOCK_PREFERENCES, keysyms
from pango import WEIGHT_NORMAL, WEIGHT_BOLD

from SCRIBES.Trigger import Trigger
from SCRIBES.TriggerManager import TriggerManager
from SCRIBES.TriggerSystem.AcceleratorActivator import Activator
from SCRIBES.Utils import open_database

from scribes.helpers import connect_external, connect_all

old_create_trigger = None
shortcuts = {}

def new_create_trigger(self, name, accelerator="", description="", category="", error=True, removable=True):
    if name in shortcuts:
        accelerator = shortcuts[name]

    return old_create_trigger(self, name, accelerator, description, category, error, removable)

# Very tricky, very dirty. Don't do that.
def find_objects_of(cls):
    for r in gc.get_referrers(cls):
        if isinstance(r, cls):
            yield r

def replace_accelerator(name, new_accel, startup):
    activators = dict((a._Activator__editor, a) for a in find_objects_of(Activator))
    for t in find_objects_of(Trigger):
        if t.name == name:
            a = activators[t._Trigger__editor]
            
            trigger_in = t in a._Activator__dictionary.values()
            
            a._Activator__remove(t)
            t._Trigger__accelerator = new_accel
            
            if not startup or trigger_in:
                a._Activator__add(t)

class Plugin(object):
    already_loaded = False

    def __init__(self, editor):
        self.editor = editor
        self.gui = None

    def replace_existing_triggers(self):
        for t in find_objects_of(Trigger):
            if t.name in shortcuts:
                replace_accelerator(t.name, shortcuts[t.name], True)

    def patch_trigger_manager(self):
        global old_create_trigger
        old_create_trigger = TriggerManager.create_trigger
        TriggerManager.create_trigger = new_create_trigger

    def init_gui(self):
        if not self.gui:
            self.gui = self.editor.get_gui_object(globals(), 'gui.glade')
            self.gui.connect_signals(self)
            
            self.window = self.gui.get_object('ActionWindow')
            self.actions = self.gui.get_object('actions_store')
            self.actions_view = self.gui.get_object('actions_treeview')
            
            self.actions_view.get_column(1).get_cell_renderers()[0].props.editable = True
            
    def add_preferences_menu_item(self):
        item = self.editor.create_menuitem('Key configuration', STOCK_PREFERENCES)
        self.editor.add_to_pref_menu(item)
        connect_all(self, menuitem=item)
    
    @connect_external('menuitem', 'activate')    
    def show_shortcuts_window(self, *args):
        self.init_gui()
        
        self.actions_view.set_model(None)
        self.actions.clear()
        
        category = {}
        sortkey = lambda v: (v.category if v.category else 'Without category') + v.name
        
        for t in sorted(self.editor.triggers, key=sortkey):
            if not t.category in category:
                category[t.category] = self.actions.append(
                    None, (t.category, None, None, False, WEIGHT_NORMAL))
            
            self.actions.append(category[t.category], (t.name, t.accelerator, t.description,
                True, WEIGHT_BOLD if t.name in shortcuts else WEIGHT_NORMAL))    
        
        self.actions_view.set_model(self.actions)
        self.actions_view.expand_all()
        
        self.window.show()
    
    def hide_shortcuts_window(self):
        self.save_shortcuts()
        self.window.hide()
        
    def on_key_press_event(self, window, event):
        if event.keyval == keysyms.Escape:
            self.hide_shortcuts_window()
            return True
    
        return False
        
    def on_delete_event(self, *args):
        self.hide_shortcuts_window()
        return True

    def load(self):
        if not Plugin.already_loaded:
            Plugin.already_loaded = True
            self.load_shortcuts()
            self.replace_existing_triggers()
            self.patch_trigger_manager()

        self.add_preferences_menu_item()            
        self.editor.show_full_view()

    def on_accel_edited(self, renderer, path, accel_key, accel_mods, hardware_keycode):
        iter = self.actions.get_iter(path)
        accel = accelerator_name(accel_key, accel_mods)
        name = self.actions.get_value(iter, 0)
        
        shortcuts[name] = accel
        
        self.actions.set_value(iter, 1, accel)
        self.actions.set_value(iter, 4, WEIGHT_BOLD)
        
        replace_accelerator(name, accel, False)
    
    def on_accel_cleared(self, renderer, path, *args):
        iter = self.actions.get_iter(path)
        name = self.actions.get_value(iter, 0)
        
        shortcuts[name] = None
        
        self.actions.set_value(iter, 1, None)
        self.actions.set_value(iter, 4, WEIGHT_BOLD)
        
        replace_accelerator(name, None, False)

    def get_db(self, mode='r'):
        return open_database(os.path.join("PluginPreferences", "Shortcuts", "shortcuts.gdb"), mode)
    
    def load_shortcuts(self):
        try:
            db = self.get_db()
            shortcuts.clear()
            for k, v in db.iteritems():
                shortcuts[k] = v
        except Exception, e:
            print e
        finally:
            db.close()

    def save_shortcuts(self):
        try:
            db = self.get_db('n')
            for k, v in shortcuts.iteritems():
                db[k] = v
        except Exception, e:
            print e
        finally:
            db.close()
