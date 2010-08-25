import sys

from SCRIBES.TriggerManager import TriggerManager

from .weak import weak_connect
from .signals import Signal, Trigger, SignalManager, connect_triggers

class Plugin(object):
    def __init__(self, editor):
        editor.response()
        self.editor = editor
        self.triggers = TriggerManager(editor)
        editor.response()
        
        connect_triggers(self, self.triggers)
    
    def load(self):
        pass

    def unload(self):
        self.triggers.remove_triggers()


def bootstrap(plugin_class_name):
    '''
    Returns bootstrap class to eliminate modules loading overhead during plugin init
    
    For example in main plugin module (PluginTest.py) you may write:

        class_name = "TestPlugin"
        
        TestPlugin = bootstrap(Test.RealTestPlugin)
        
    Also fuction helps to remove some repeating code
    
    @param plugin_class_name: full qualified plugin class name  
    @return Bootstrap class
    '''
    class Bootstrap(object):
        def __init__(self, editor):
            editor.response()
            self.editor = editor
            editor.response()
            self.plugin = None
            
        def load(self):
            module_name, class_name = plugin_class_name.rsplit('.', 1)
            
            if module_name not in sys.modules: 
                __import__(module_name)
            
            module = sys.modules[module_name]
            cls = getattr(module, class_name)
            
            self.plugin = cls(self.editor)
            self.plugin.load()
            
        def unload(self):
            self.plugin.unload()
            self.plugin = None

    return Bootstrap
