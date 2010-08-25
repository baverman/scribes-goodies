import gobject

from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL
from SCRIBES.TriggerManager import TriggerManager as CoreTriggerManager

from .weak import weak_connect

def append_attr(obj, attr, value):
    """
    Appends value to object attribute
    
    Attribute may be undefined
    
    For example:
        append_attr(obj, 'test', 1)
        append_attr(obj, 'test', 2)
        
        assert obj.test == [1, 2]
    """
    try:
        getattr(obj, attr).append(value)
    except AttributeError:
        setattr(obj, attr, [value])
        

def attach_signal_connect_info(attr, obj, func, after, idle, idle_priority):
    """
    Adds signal connection info to function
    
    Used by signal and trigger decorators
    """
    connect_params = dict(after=after, idle=idle, idle_priority=idle_priority)

    if func:
        if not getattr(func, '__call__'):
            raise Exception('Signal decorator accept callable or connect params')
        
        append_attr(func, attr, (obj, connect_params))
        return func
    else:
        def inner(func):
            append_attr(func, attr, (obj, connect_params))
            return func
        
        return inner    
    

class Signal(object):
    """
    Unbounded signal
    
    Class only holds signal parameters which used to instantiate correct GObject
    """
    
    def __init__(self, arg_count=0):
        """
        @param arg_count: Signal argument count. Default is zero.  
        """
        self.signal_type = SSIGNAL
        self.return_type = TYPE_NONE
        self.arg_types = tuple(TYPE_PYOBJECT for r in range(arg_count))
        self.name = None

    def __call__(self, func=None, after=False, idle=True, idle_priority=None):
        """
        Decorator to mark class methods as callbacks to this signal
        
        Usage:
            @signal
            def callback(...): pass # Connects signal with idle wrapper
            
            @signal(idle=False)
            def callback(...): pass # Usual (in gobject terms) signal connection
            
            @signal(after=True)
            def callback(...): pass # sender.connect_after(callback) analog
            
            @signal(idle_priority=9999)
            def callback(...): pass # idle wrapper will start callback with specified priority
            
        And you may combine connect parameters of course
        """
        return attach_signal_connect_info('signals_to_connect',
            self, func, after, idle, idle_priority)


class SignalManager(object):
    """
    Wrapper for inner GObject with signals
    
    Example:
        class Manager(SignalManager):
            show = Signal()
            hide = Signal()
        
    Manager.show and Manager.hide is unbounded signals and can be used as
    decorators to callbacks. Whereas instance.show and instance.hide is bounded and
    can be used to emit signals. 
    
        class Plugin(object):
            def __init__(self):
                self.signals = Manager()
                self.signals.connect_signals()
                
                self.signals.hide.emit() 
                
            @Manager.show
            def show(self, sender):
                pass
                
    Inner GObject with necessary __gsignals__ is constructed during instance initialization
    """
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
        """
        Connects marked object methods
        """
        for attr, value in obj.__class__.__dict__.iteritems():
            for signal, connect_params in getattr(value, 'signals_to_connect', ()):
                self.connect(signal, obj, attr, **connect_params)    

    def connect(self, signal, obj, attr, after, idle, idle_priority):
        """
        Connects unbounded signal
        
        @param signal: Unbounded signal
        """
        weak_connect(self.sender, signal.name, obj, attr,
            after=after, idle=idle, idle_priority=idle_priority)


class BoundedSignal(object):
    """
    This class knows about its GObject wrapper and unbounded signal name
    
    This allows it to emit signals 
    """
    def __init__(self, manager, signal):
        self.manager = manager
        self.signal = signal

    def connect(self, obj, attr, after, idle, idle_priority):
        self.manager.connect(self.signal, obj, attr,
            after=after, idle=idle, idle_priority=idle_priority)

    def emit(self, *args):
        self.manager.sender.emit(self.signal.name, *args)

    
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
        
    def __call__(self, func=None, after=False, idle=True, idle_priority=None):
        return attach_signal_connect_info('triggers_to_connect',
            self, func, after, idle, idle_priority)
            
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
        
    def connect(self, trigger, obj, attr, after, idle, idle_priority):
        if trigger.name not in self.triggers:
            self.triggers[trigger.name] = trigger.create(self.manager)
    
        weak_connect(self.triggers[trigger.name], 'activate', obj, attr,
            after=after, idle=idle, idle_priority=idle_priority)
