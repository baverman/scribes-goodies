from gobject import idle_add
from scribes_helpers import weak_connect 

from .Utils import BOOKMARK_NAME

class Updater(object):
    def __init__(self, signals, editor):
        self.editor = editor
        self.signals = signals
        self.buffer = editor.textbuffer
        self.lines = ()
        
        weak_connect(editor.textbuffer, 'source-mark-updated', self, 'update',
            after=True, idle_priority=9999)

        weak_connect(editor, 'modified-file', self, 'update',
            after=True, idle_priority=9999999)

        weak_connect(editor, 'renamed-file', self, 'update',
            after=True, idle_priority=9999)

        idle_add(self.optimize, priority=9999)

    def line_from(self, mark):
        iter_at_mark = self.buffer.get_iter_at_mark
        return iter_at_mark(mark).get_line()

    def get_bookmarked_lines(self):
        mark = self.find_first_mark()
        marks = self.get_all_marks(mark)
        lines = [self.line_from(mark) for mark in marks]
        return tuple(lines)

    def find_first_mark(self):
        iterator = self.buffer.get_bounds()[0]
        marks = self.buffer.get_source_marks_at_iter(iterator, BOOKMARK_NAME)
        if marks:
            return marks[0]
    
        found_mark = self.buffer.forward_iter_to_source_mark(iterator, BOOKMARK_NAME)
        if found_mark is False:
            raise ValueError
        
        marks = self.buffer.get_source_marks_at_iter(iterator, BOOKMARK_NAME)
        
        return marks[0]

    def get_all_marks(self, mark):
        marks = []
        append = marks.append
        append(mark)
        while True:
            mark = mark.next(BOOKMARK_NAME)
            if mark is None: break
            append(mark)
        return marks

    def update(self, *args):
        try:
            lines = self.get_bookmarked_lines()
        except ValueError:
            lines = ()
        finally:
            if lines == self.lines: return False
            self.lines = lines
            self.signals.lines.emit(lines)
        return False

    def optimize(self):
        methods = (
            self.update, self.get_bookmarked_lines,
            self.find_first_mark, self.get_all_marks,
        )
        self.editor.optimize(methods)
        return False
