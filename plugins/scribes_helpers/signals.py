import gobject

from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

from .weak import weak_connect

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


def append_attr(obj, attr, value):
    try:
        getattr(obj, attr).append(value)
    except AttributeError:
        setattr(obj, attr, [value])
        
    
class Trigger(object):
    def __init__(self, *args):
        self.args = args
        self.trigger = None
        
    def __call__(self, func=None, after=False, idle=True, idle_priority=None):
        connect_params = dict(after=after, idle=idle, idle_priority=idle_priority)

        if func:
            if not getattr(func, '__call__'):
                raise Exception('Trigger decorator accept callable or connect params')
            
            append_attr(func, 'triggers_to_connect', (self, connect_params))
            return func
        else:
            def inner(func):
                append_attr(func, 'triggers_to_connect', (self, connect_params))
                return func
            
            return inner    
    
    def connect(self, trigger_manager, obj, attr, after, idle, idle_priority):
        if not self.trigger: 
            self.trigger = trigger_manager.create_trigger(*self.args)
    
        weak_connect(self.trigger, 'activate', obj, attr,
            after=after, idle=idle, idle_priority=idle_priority)
        

class BoundedSignal(object):
    def __init__(self, manager, signal):
        self.manager = manager
        self.signal = signal

    def __call__(self, func=None, after=False, idle=True, idle_priority=None):
        connect_params = dict(after=after, idle=idle, idle_priority=idle_priority)

        if func:
            if not getattr(func, '__call__'):
                raise Exception('Signal decorator accept callable or connect params')
            
            append_attr(func, 'signals_to_connect', (self, connect_params))
            return func
        else:
            def inner(func):
                append_attr(func, 'signals_to_connect', (self, connect_params))
                return func
            
            return inner    

    def connect(self, obj, attr, after, idle, idle_priority):
        weak_connect(self.manager.sender, self.signal.name, obj, attr,
            after=after, idle=idle, idle_priority=idle_priority)

    def emit(self, *args):
        self.manager.sender.emit(self.signal.name, *args)
        
        
def connect_signals(obj):
    for k, v in obj.__class__.__dict__.iteritems():
        for signal, connect_params in getattr(v, 'signals_to_connect', ()):
            signal.connect(obj, k, **connect_params)        

def connect_triggers(obj, manager):
    for k, v in obj.__class__.__dict__.iteritems():
        for trigger, connect_params in getattr(v, 'triggers_to_connect', ()):
            trigger.connect(manager, obj, k, **connect_params)
