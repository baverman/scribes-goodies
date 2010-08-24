import weakref
import gobject
from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL
from SCRIBES.TriggerManager import TriggerManager
from types import FunctionType

class WeakCallback (object):
    def __init__(self, obj, attr):
        self.wref = weakref.ref(obj)
        self.callback_attr = attr
        self.gobject_token = None
        self.dbus_token = None

    def __call__(self, *args, **kwargs):
        obj = self.wref()
        if obj:
            attr = getattr(obj, self.callback_attr)
            attr(*args, **kwargs)
        elif self.gobject_token:
            sender = args[0]
            sender.disconnect(self.gobject_token)
            self.gobject_token = None
        elif self.dbus_token:
            self.dbus_token.remove()
            self.dbus_token = None


def gobject_connect_weakly(sender, signal, connector, attr, *user_args):
    wc = WeakCallback(connector, attr)
    wc.gobject_token = sender.connect(signal, wc, *user_args)


class Signal(object):
    def __init__(self, arg_count=0):
        self.signal_type = SSIGNAL
        self.return_type = TYPE_NONE
        self.arg_types = tuple(TYPE_PYOBJECT for r in range(arg_count))
        self.name = None


class SignalManager(object):
    def __init__(self):    
        signals = {}
        for k, v in self.__class__.__dict__.iteritems():
            if isinstance(v, Signal):
                v.name = k.replace('_', '-')
                signals[v.name] = (v.signal_type, v.return_type, v.arg_types)
                setattr(self, k, BoundedSignal(self, v))
        
        if signals:
            classname = self.__class__.__name__ + 'Signals'
            cls = type(classname, (GObject,), {'__gsignals__':signals})
            gobject.type_register(cls)
            self.sender = cls()
        else:
            raise Exception('Empty signal manager')

        
class Trigger(object):
    def __init__(self, *args):
        self.args = args
        self.trigger = None
        
    def __call__(self, func):
        func.trigger_to_connect = self
        return func
    
    def connect(self, trigger_manager, obj, attr):
        if not self.trigger: 
            self.trigger = trigger_manager.create_trigger(*self.args)
    
        gobject_connect_weakly(self.trigger, 'activate', obj, attr)
        

class BoundedSignal(object):
    def __init__(self, manager, signal):
        self.manager = manager
        self.signal = signal

    def __call__(self, func):
        func.signal_to_connect = self
        return func

    def connect(self, obj, attr):
        gobject_connect_weakly(self.manager.sender, self.signal.name, obj, attr)

    def emit(self, *args):
        self.manager.sender.emit(self.signal.name, *args)



class Plugin(object):
    def __init__(self, editor):
        editor.response()
        self.editor = editor
        self.triggers = TriggerManager(editor)
        editor.response()
    
    def connect_signals(self):
        for k, v in self.__class__.__dict__.iteritems():
            signal = getattr(v, 'signal_to_connect', None)
            if signal:
                signal.connect(self, k)        

    def connect_triggers(self):
        for k, v in self.__class__.__dict__.iteritems():
            trigger = getattr(v, 'trigger_to_connect', None)
            if trigger:
                trigger.connect(self.triggers, self, k)        
        
    def load(self):
        self.connect_signals()
        self.connect_triggers()

    def unload(self):
        self.triggers.remove_triggers()
