import sys, os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import weakref
import gtk
import gc

import unittest

from gsignals import Signal, SignalManager


def refresh_gui():
    """
    Magic function to emulate gtk main loop
    """
    while gtk.events_pending():
        gtk.main_iteration_do(block=False)
  

class Signals(SignalManager):
    test1 = Signal()
    test2 = Signal()
    

class SignalChecker(object):
    def __init__(self):
        self.signals = {}
        
    def clear(self):
        self.signals.clear()
        
    def fired(self, name):
        return name in self.signals            
    
    def fire(self, name):
        self.signals[name] = True


class Plugin(object):
    
    def __init__(self, signals, checker):
        self.signals = signals
        signals.connect_signals(self)
        self.checker = checker
    
    @Signals.test1
    def test1(self, *args):
        self.checker.fire('test1')
    
    @Signals.test2
    def test2(self, *args):
        self.checker.fire('test2')
        
        
class TestCase(unittest.TestCase):
    
    def test_plugin_deletion(self):
        checker = SignalChecker()
        
        # This trick allows to brake direct refs from current stack frame
        signal_holder = [Signals()]
        wsignals = weakref.ref(signal_holder[0]) # to check signal manager deletion
        wsender = weakref.ref(wsignals().sender) # to check signal manager GObject deletion
        
        plugin_holder = [Plugin(wsignals(), checker)] 
        wplugin = weakref.ref(plugin_holder[0]) # to check plugin deletion
        
        test1_handler_id = wplugin().test1_handler.id
        test2_handler_id = wplugin().test2_handler.id
        
        # There is can be only one ref from holder list
        plugin_references = gc.get_referrers(wplugin())
        self.assertEquals(len(plugin_references), 1)
        self.assertTrue(plugin_references[0] is plugin_holder)
        
        wsignals().test1.emit()
        refresh_gui()
        self.assertTrue(checker.fired('test1'))
        
        # Now we unload plugin by eleminating direct refs.
        # In our case simply clear holder list
        plugin_holder[:] = []
        checker.clear()
        
        self.assertEqual(wplugin(), None) # plugin really deleted
        
        # At this point we have Signals GObject connected to plugin callbacks
        self.assertTrue(wsignals().sender.handler_is_connected(test1_handler_id))
        self.assertTrue(wsignals().sender.handler_is_connected(test2_handler_id))
        
        # But after emmiting signal it is automatically disconnected
        wsignals().test2.emit()
        refresh_gui()
        self.assertFalse(checker.fired('test2'))
        self.assertTrue(wsender().handler_is_connected(test1_handler_id))
        self.assertFalse(wsender().handler_is_connected(test2_handler_id))
        
        # Removing refs to signal manager. Manager and its GObject must vanish 
        signal_holder[:] = []
        self.assertEqual(wsignals(), None) # Signal manager really deleted
        self.assertEqual(wsender(), None) # GObject really deleted
        
        
if __name__ == '__main__':
    unittest.main()  
