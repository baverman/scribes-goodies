from scribes_helpers import SignalManager, Signal

class Signals(SignalManager):
    destroy        = Signal()
    toggle         = Signal()
    remove_all     = Signal()
    show           = Signal()
    hide           = Signal()
    add            = Signal(1)
    remove         = Signal(1)
    lines          = Signal(1)
    bookmark_lines = Signal(1)
    feedback       = Signal(1)
    model_data     = Signal(1)
    scroll_to_line = Signal(1)
    updated_model  = Signal()
