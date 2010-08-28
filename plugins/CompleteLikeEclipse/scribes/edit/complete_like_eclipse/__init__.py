from gettext import gettext as _
from string import whitespace

from scribes.helpers import TriggerManager, Trigger, weak_connect 

from signals import Signals 


from IndexerProcessManager import Manager as IndexerProcessManager
from DictionaryManager import Manager as DictionaryManager
from ProcessCommunicator import Communicator as ProcessCommunicator
from TextExtractor import Extractor as TextExtractor
from BufferMonitor import Monitor as BufferMonitor


trigger = Trigger('complete-word', '<alt>slash',
    'Eclipse like word completition', 'Text Operations')

class Plugin(object):
    def __init__(self, editor):
        self.editor = editor
        self.signals = Signals()
        self.signals.connect_signals(self)
        
        self.triggers = TriggerManager(editor)
        self.triggers.connect_triggers(self)
        
        self.block_word_reset = False
        self.words = None
        self.start_word = None
        self.start_offset = None
        
        self.indexer = IndexerProcessManager(self.signals.sender, editor)
        self.dictionary_manager = DictionaryManager(self.signals.sender, editor)
        self.communicator = ProcessCommunicator(self.signals.sender, editor)
        self.extractor = TextExtractor(self.signals.sender, editor)
        self.buffer_monitor = BufferMonitor(self.signals.sender, editor)
        
        weak_connect(self.editor.textbuffer, 'changed', self, 'buffer_changed')

    def unload(self):
        self.signals.destroy.emit()
        return False
    
    def is_valid_character(self, c):
        if c in whitespace:
            return False
        
        return c.isalpha() or c.isdigit() or (c in ("-", "_"))

    def backward_to_word_begin(self, iterator):
        if iterator.starts_line(): return iterator
        iterator.backward_char()
        while self.is_valid_character(iterator.get_char()):
            iterator.backward_char()
            if iterator.starts_line(): return iterator
        iterator.forward_char()
        return iterator

    def forward_to_word_end(self, iterator):
        if iterator.ends_line(): return iterator
        if not self.is_valid_character(iterator.get_char()): return iterator
        while self.is_valid_character(iterator.get_char()):
            iterator.forward_char()
            if iterator.ends_line(): return iterator
        return iterator
    
    def get_word_before_cursor(self):
        iterator = self.editor.cursor.copy()
        # If the cursor is in front of a valid character we ignore
        # word completion.
        if self.is_valid_character(iterator.get_char()):
            return None, None
        
        if iterator.starts_line():
            return None, None
    
        iterator.backward_char()
        
        if not self.is_valid_character(iterator.get_char()):
            return None, None
    
        start = self.backward_to_word_begin(iterator.copy())
        end = self.forward_to_word_end(iterator.copy())
        word = self.editor.textbuffer.get_text(start, end).strip()
        
        return word, start

    def get_matches(self, string):
        if not self.words:
            return None
        
        result = []
        for word, count in self.words.iteritems():
            if word != string and word.startswith(string):
                result.append((word.encode('utf8'), count))
                
        result.sort(key=lambda r: r[1], reverse=True)
        
        return [r[0] for r in result]

    @trigger
    def cycle(self, *args):
        word_to_complete, start = self.get_word_before_cursor()
        
        if not word_to_complete:
            return False

        if not self.start_word or self.start_offset != start.get_offset():
            self.start_word = word_to_complete
            self.start_offset = start.get_offset()

        matches = self.get_matches(self.start_word)
        if matches:
            idx = 0
            try:
                idx = matches.index(word_to_complete)
                idx = (idx + 1) % len(matches)
            except ValueError:
                pass

            if matches[idx] == word_to_complete:
                self.editor.update_message(_("Word completed already"), "yes", 1)
                return False
                
            self.block_word_reset = True             
            
            end = self.editor.cursor.copy()
            self.editor.textbuffer.delete(start, end)
            self.editor.textbuffer.insert(start, matches[idx])
            
            self.editor.response()
            self.block_word_reset = False
        else:
            self.editor.update_message(_("No word to complete"), "no", 1)

        return False
    
    @Signals.dictionary
    def word_list_updated(self, sender, words):
        self.words = words
        return False
        
    def buffer_changed(self, *args):
        if not self.block_word_reset and self.start_word:
            self.start_word = None
            self.start_iter = None
        
        return False
