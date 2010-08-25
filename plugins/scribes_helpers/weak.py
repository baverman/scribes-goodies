import weakref
from gobject import idle_add

class WeakCallback (object):
    def __init__(self, obj, attr, idle, idle_priority):
        self.wref = weakref.ref(obj)
        self.callback_attr = attr
        self.gobject_token = None
        self.dbus_token = None
        self.idle = idle
        self.idle_priority = idle_priority

    def __call__(self, *args, **kwargs):
        obj = self.wref()
        if obj:
            attr = getattr(obj, self.callback_attr)
            
            if self.idle:
                if self.idle_priority:
                    idle_add(attr, priority=self.idle_priority, *args, **kwargs)
                else:
                    idle_add(attr, *args, **kwargs)
            else:
                return attr(*args, **kwargs)
                    
        elif self.gobject_token:
            sender = args[0]
            sender.disconnect(self.gobject_token)
            self.gobject_token = None
        elif self.dbus_token:
            self.dbus_token.remove()
            self.dbus_token = None
            
        return False


def weak_connect(sender, signal, connector, attr, idle=True, after=False, idle_priority=None):
    if idle_priority:
        idle = True
    
    wc = WeakCallback(connector, attr, idle, idle_priority)
    
    if after:
        wc.gobject_token = sender.connect_after(signal, wc)
    else:
        wc.gobject_token = sender.connect(signal, wc)
        
    #print "Connected", sender, signal, connector, attr, idle, after, idle_priority
