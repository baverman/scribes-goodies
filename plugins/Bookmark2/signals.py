from scribes_helpers import SignalManager, Signal

class Signals(SignalManager):
    destroy        = Signal()
    toggle         = Signal()
    remove_all     = Signal(1)
    show           = Signal()
    hide           = Signal()
    add            = Signal(2)
    remove         = Signal(2)
    lines          = Signal(1)
    bookmark_lines = Signal(1)
    model_data     = Signal(1)
    scroll_to_line = Signal(1)
    updated_model  = Signal()
