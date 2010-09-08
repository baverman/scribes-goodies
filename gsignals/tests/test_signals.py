import sys
import unittest

import gtk
import gobject

from gsignals import Signal, SignalManager, connect_external, connect_all
from gsignals.signals import SSIGNAL


def refresh_gui():
    """
    Magic function to emulate gtk main loop
    """
    while gtk.events_pending():
        gtk.main_iteration_do(block=False)


class Case(unittest.TestCase):
    
    def test_signal_simple_creation(self):
        s = Signal()
        
        self.assertEqual(s.signal_type, SSIGNAL) 
        self.assertEqual(s.return_type, None)
        self.assertEqual(s.arg_types, ())

    def test_signal_creation_with_arguments(self):
        s = Signal(object, int)
        
        self.assertEqual(s.signal_type, SSIGNAL) 
        self.assertEqual(s.return_type, None)
        self.assertEqual(s.arg_types, (object, int))

    def test_signal_creation_with_return_type(self):
        s = Signal(return_type=object)
        
        self.assertEqual(s.signal_type, SSIGNAL) 
        self.assertEqual(s.return_type, object)
        self.assertEqual(s.arg_types, ())

    def test_signal_creation_with_signal_type(self):
        s = Signal(type=gobject.SIGNAL_ACTION)
        
        self.assertEqual(s.signal_type, gobject.SIGNAL_ACTION) 
        self.assertEqual(s.return_type, None)
        self.assertEqual(s.arg_types, ())
        
    def test_simple_autoconnecting_and_emmiting_case(self):
        
        class Signals(SignalManager):
            hide = Signal(int)
            show = Signal()
            
        class Handler(object):
            def __init__(self):
                self.signals = Signals()
                connect_all(self, self.signals)
                
                self.hided = None
                self.showed = None
            
            @Signals.hide(idle=True)
            def hide(self, sender, arg):
                self.hided = arg
            
            @Signals.show
            def show(self, *args):
                self.showed = True
            
        h = Handler()
        
        h.signals.show.emit()
        self.assertTrue(h.showed)
        
        h.signals.hide.emit(5)
        # callback will be called after event loop processing because idle wrapper
        self.assertEqual(h.hided, None)
        refresh_gui()
        self.assertEqual(h.hided, 5)
        
    def test_autoconnecting_to_external_signals(self):
        class Signals1(SignalManager):
            fire = Signal()
            
        class Signals2(SignalManager):
            fire = Signal()
        
        class Handler(object):
            def __init__(self, s1, s2):
                self.fired = 0
                connect_all(self, sender1=s1, sender2=s2)
            
            @connect_external('sender1', 'fire')
            @connect_external('sender2', 'fire', idle=True)
            def fire(self, *args):
                self.fired += 1

        s1 = Signals1()
        s2 = Signals2()
        h = Handler(s1.sender, s2.sender)
        
        s1.fire.emit()
        self.assertEqual(h.fired, 1)
        
        s2.fire.emit()
        self.assertEqual(h.fired, 1)
        refresh_gui()
        self.assertEqual(h.fired, 2)
        
    def test_signals_blocking(self):
        class Signals(SignalManager):
            fire = Signal()
            
        class Handler(object):
            def __init__(self):
                self.fired = 0
                self.signals = Signals()
                self.signals.connect_signals(self)
            
            @Signals.fire
            def fire(self, *args):
                self.fired += 1

        h = Handler()

        h.fire.handler.block()
        h.signals.fire.emit()
        self.assertEqual(h.fired, 0)
        
        h.fire.handler.unblock()
        h.signals.fire.emit()
        self.assertEqual(h.fired, 1)

    def test_several_signals_blocking(self):
        class FireSignals(SignalManager):
            fire = Signal()

        class WaterSignals(SignalManager):
            water = Signal()
            
        class Handler(object):
            def __init__(self, water):
                self.fired = 0
                self.signals = FireSignals()
                
                connect_all(self, self.signals, water=water.sender)
            
            @FireSignals.fire
            @connect_external('water', 'water')
            def fire(self, *args):
                self.fired += 1

        w = WaterSignals()
        h = Handler(w)

        self.assertRaises(Exception, h.fire.handler.block)
        
        h.fire.handler(signal_name='fire').block()
        w.water.emit()
        h.signals.fire.emit()
        self.assertEqual(h.fired, 1)
        
        h.fire.handler(signal_name='fire').unblock()
        w.water.emit()
        h.signals.fire.emit()
        self.assertEqual(h.fired, 3)
        
        h.fire.handler(sender_name='water').block()
        w.water.emit()
        h.signals.fire.emit()
        self.assertEqual(h.fired, 4)
        
        h.fire.handler(sender_name='water').unblock()
        w.water.emit()
        h.signals.fire.emit()
        self.assertEqual(h.fired, 6)
        
        h.fire.handler(sender=w.sender).block()
        w.water.emit()
        h.signals.fire.emit()
        self.assertEqual(h.fired, 7)        
