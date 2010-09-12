from gsignals import weak_connect, connect_all as gsignals_connect_all
from gsignals.signals import attach_signal_connect_info

from SCRIBES.TriggerManager import TriggerManager as CoreTriggerManager

def connect_all(obj, *managers, **external_gobjects):
    for m in managers:
        if isinstance(m, TriggerManager):
            m.connect_triggers(obj)
        else:
            m.connect_signals(obj)

    gsignals_connect_all(obj, **external_gobjects)


class Trigger(object):
    """
    Unbounded trigger (special signal emited by keyboard shortcut)
    
    Can be used as decorator to mark methods for feature connecting. 
    """
    def __init__(self, name, accelerator="", description="", category="",
            error=True, removable=True):
        self.name = name
        self.accelerator = accelerator 
        self.description = description
        self.category = category
        self.error = error
        self.removable = removable
        
    def __call__(self, func=None, after=False, idle=False):
        return attach_signal_connect_info('triggers_to_connect', self, func, after, idle)
            
    def create(self, manager):
        return manager.create_trigger(self.name, self.accelerator, self.description,
            self.category, self.error, self.removable)


class TriggerManager(object):
    '''
    Auto disconnected trigger manager
    
    Wraps SCRIBES.TriggerManager and calls remove_triggers on object deletion 
    '''
    def __init__(self, editor):
        self.manager = CoreTriggerManager(editor)
        self.triggers = {}

    def __del__(self):
        self.triggers.clear()
        self.manager.remove_triggers()
    
    def connect_triggers(self, obj):
        '''
        Connects object methods marked by trigger decorator  
        '''
        for attr, value in obj.__class__.__dict__.iteritems():
            for trigger, connect_params in getattr(value, 'triggers_to_connect', ()):
                self.connect(trigger, obj, attr, **connect_params)
        
    def connect(self, trigger, obj, attr, after, idle):
        if trigger.name not in self.triggers:
            self.triggers[trigger.name] = trigger.create(self.manager)
    
        weak_connect(self.triggers[trigger.name], 'activate', obj, attr, after=after, idle=idle)
