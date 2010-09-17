import gc

from gtk import accel_groups_from_object, accelerator_parse, accelerator_name
from gtk import ACCEL_LOCKED, STOCK_PREFERENCES
from pango import WEIGHT_NORMAL, WEIGHT_BOLD

from SCRIBES.Trigger import Trigger
from SCRIBES.TriggerManager import TriggerManager
from SCRIBES.TriggerSystem.AcceleratorActivator import Activator

from scribes.helpers import connect_external, connect_all

old_create_trigger = None
shortcuts = {
    'show-quick-open-window': '<ctrl><alt>r'
}

def new_create_trigger(self, name, accelerator="", description="", category="", error=True, removable=True):
    if name in shortcuts:
        accelerator = shortcuts[name]

    return old_create_trigger(self, name, accelerator, description, category, error, removable)

# Very tricky, very dirty. Don't do that.
def find_objects_of(cls):
    for r in gc.get_referrers(cls):
        if isinstance(r, cls):
            yield r

def replace_accelerator(old_accel, new_accel, trigger=None):
    old_accel = accelerator_parse(old_accel)
    for a in find_objects_of(Activator):
        if old_accel in a._Activator__dictionary:
            trigger = a._Activator__dictionary[old_accel]
            a._Activator__remove(trigger)

            trigger._Trigger__accelerator = new_accel
    
            print 'Replaced ', trigger.name, trigger.accelerator
            a._Activator__add(trigger)
        else:
            trigger._Trigger__accelerator = new_accel
            print 'too fast ', trigger.name, trigger.accelerator


class Plugin(object):
    already_loaded = False

    def __init__(self, editor):
        self.editor = editor
        self.gui = None

    def replace_existing_triggers(self):
        for t in find_objects_of(Trigger):
            if t.name in shortcuts:
                replace_accelerator(t.accelerator, shortcuts[t.name], t)

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
        
        for t in sorted(self.editor.triggers, key=lambda v: (v.category if v.category else 'Without category') + v.name):
            if not t.category in category:
                category[t.category] = self.actions.append(None, (t.category, None, None, False, 400))
            
            self.actions.append(category[t.category], (t.name, t.accelerator, t.description,
                True, WEIGHT_BOLD if t.name in shortcuts else WEIGHT_NORMAL))    
        
        self.actions_view.set_model(self.actions)
        self.actions_view.expand_all()
        
        self.window.show()
    
    def load(self):
        if not Plugin.already_loaded:
            Plugin.already_loaded = True

            self.replace_existing_triggers()
            self.patch_trigger_manager()

        self.add_preferences_menu_item()            
        self.editor.show_full_view()

    def on_accel_edited(self, renderer, path, accel_key, accel_mods, hardware_keycode):
        iter = self.actions.get_iter(path)
        accel = accelerator_name(accel_key, accel_mods)
        name = self.actions.get_value(iter, 0)
        old_accel = self.actions.get_value(iter, 1)
        
        print name, accel
        shortcuts[name] = accel
        
        self.actions.set_value(iter, 1, accel)
        self.actions.set_value(iter, 4, WEIGHT_BOLD)
        
        replace_accelerator(old_accel, accel)
        
