from gobject import timeout_add

from scribes_helpers import connect_signals, weak_connect 
from signals import signals


class Reseter(object):

	def __init__(self, editor):
		editor.response()
		self.editor = editor
		
		self.lines = ()
		self.update = True
		
		weak_connect(editor, "reset-buffer", self, 'reset_buffer') 
		connect_signals(self)

	def reset_buffer(self, editor, operation):
		if operation == "begin":
			self.update = False
			signals.feedback.emit(False)
		else:
			signals.remove_all.emit()
			signals.bookmark_lines.emit(self.lines)
			self.update = True
			timeout_add(250, self.enable_feedback, priority=9999)
		return False

	def enable_feedback(self):
		signals.feedback.emit(True)
		return False

	@signals.lines
	def lines_cb(self, sender, lines):
		if self.update:
		    self.lines = lines
		    
		return False
