import gobject

from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

from .weak import weak_connect

def append_attr(obj, attr, value):
    try:
        getattr(obj, attr).append(value)
    except AttributeError:
        setattr(obj, attr, [value])
        

class Signal(object):
    def __init__(self, arg_count=0):
        self.signal_type = SSIGNAL
        self.return_type = TYPE_NONE
        self.arg_types = tuple(TYPE_PYOBJECT for r in range(arg_count))
        self.name = None

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


class SignalManager(object):
    def __init__(self):    
        signals = {}
        for sname, signal in self.__class__.__dict__.iteritems():
            if isinstance(signal, Signal):
                signal.name = sname.replace('_', '-')
                signals[signal.name] = (signal.signal_type,
                    signal.return_type, signal.arg_types)
                
                setattr(self, sname, BoundedSignal(self, signal))
        
        if signals:
            classname = self.__class__.__name__
            cls = type(classname, (GObject,), {'__gsignals__':signals})
            gobject.type_register(cls)
            self.sender = cls()
        else:
            raise Exception('Empty signal manager')
            
    def connect_signals(self, obj):
        for attr, value in obj.__class__.__dict__.iteritems():
            for signal, connect_params in getattr(value, 'signals_to_connect', ()):
                self.connect(signal, obj, attr, **connect_params)    

    def connect(self, signal, obj, attr, after, idle, idle_priority):
        weak_connect(self.sender, signal.name, obj, attr,
            after=after, idle=idle, idle_priority=idle_priority)


class BoundedSignal(object):
    def __init__(self, manager, signal):
        self.manager = manager
        self.signal = signal

    def connect(self, obj, attr, after, idle, idle_priority):
        self.manager.connect(self.signal, obj, attr,
            after=after, idle=idle, idle_priority=idle_priority)

    def emit(self, *args):
        self.manager.sender.emit(self.signal.name, *args)

    
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

        
def connect_triggers(obj, manager):
    for k, v in obj.__class__.__dict__.iteritems():
        for trigger, connect_params in getattr(v, 'triggers_to_connect', ()):
            trigger.connect(manager, obj, k, **connect_params)
