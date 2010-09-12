import sys

from gsignals import weak_connect, Signal, SignalManager, connect_external
from signals import Trigger, TriggerManager, connect_all

def bootstrap(plugin_class_name):
    '''
    Returns bootstrap class to eliminate modules loading overhead during plugin init
    
    For example in main plugin module (PluginTest.py) you may write:

        class_name = "TestPlugin"
        
        TestPlugin = bootstrap(Test.RealTestPlugin)
        
    Also function helps to remove some repeating code
    
    @param plugin_class_name: full qualified plugin class name  
    @return Bootstrap class
    '''
    class Bootstrap(object):
        def __init__(self, editor):
            self.editor = editor
            self.plugin = None
            
        def load(self):
            module_name, class_name = plugin_class_name.rsplit('.', 1)
            
            if module_name not in sys.modules: 
                __import__(module_name)
            
            module = sys.modules[module_name]
            cls = getattr(module, class_name)
            
            self.plugin = cls(self.editor)
            
            if getattr(self.plugin, 'load', False):
                self.plugin.load()
            
        def unload(self):
            if getattr(self.plugin, 'unload', False):
                self.plugin.unload()
            
            self.plugin = None

    return Bootstrap
