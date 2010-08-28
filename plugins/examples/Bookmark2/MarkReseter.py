from gobject import timeout_add

from scribes_helpers import weak_connect 

from .signals import Signals


class Reseter(object):

	def __init__(self, signals, editor):
		editor.response()
		self.editor = editor
		self.signals = signals
		self.lines = ()
		self.update = True
		
		weak_connect(editor, "reset-buffer", self, 'reset_buffer') 
		signals.connect_signals(self)

	def reset_buffer(self, editor, operation):
		if operation == "begin":
			self.update = False
		else:
			self.signals.remove_all.emit(False)
			self.signals.bookmark_lines.emit(self.lines)
			self.update = True
		return False

	@Signals.lines
	def lines_cb(self, sender, lines):
		if self.update:
		    self.lines = lines
		    
		return False
