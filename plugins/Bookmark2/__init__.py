import os.path
from gettext import gettext as _
from gobject import idle_add

from scribes_helpers import Plugin, Trigger, weak_connect

from signals import signals
from Utils import create_bookmark_image, BOOKMARK_NAME

from Feedback import Feedback
from MarkReseter import Reseter
from MarkUpdater import Updater
from Marker import Marker
from GUI.Manager import Manager as GuiManager

from Metadata import set_value, get_value


trigger_toggle = Trigger("toggle-bookmark", "<ctrl>d",
    _("Add or remove bookmark on a line"), _("Bookmark Operations"))
    
trigger_show = Trigger("show-bookmark-browser", "<ctrl>b",
    _("Navigate bookmarks"), _("Bookmark Operations"))

trigger_remove = Trigger("remove-all-bookmarks", "<ctrl><alt>b",
    _("Remove all bookmarks"), _("Bookmark Operations"))


class BookmarkPlugin(Plugin):
    def __init__(self, editor):
        super(BookmarkPlugin, self).__init__(editor)
        
        # WTF? in original plugin there is no popup menu item, so commented
        #editor.textview.connect("populate-popup", self.pupulate_popup)
        
        create_bookmark_image(editor)
        
        self.feedback_manager = Feedback(editor)
        self.mark_reseter = Reseter(editor)
        self.mark_updater = Updater(editor)
        self.marker = Marker(editor)
        
        signals.sender.gui = self.gui
        self.gui_manager = GuiManager(signals.sender, editor)
        
        weak_connect(editor, "loaded-file", self, 'restore_bookmarks', idle_priority=9999)
        idle_add(self.restore_bookmarks, priority=9999)

    @property
    def gui(self):
        try:
            return self.__gui
        except AttributeError:
            self.__gui = self.editor.get_gui_object(globals(), os.path.join("GUI", "GUI.glade"))
            
        return self.__gui
        
    @trigger_toggle
    def toggle(self, sender): 
        signals.toggle.emit()
        return False

    @trigger_show
    def show(self, sender): 
        signals.show.emit()
        return False

    @trigger_remove
    def remove(self, sender): 
        signals.remove_all.emit()
        return False

    def populate_popup(self, textview, menu):
        from PopupMenuItem import PopupMenuItem
        self.editor.add_to_popup(PopupMenuItem(self.editor))
        return False
    
    @signals.scroll_to_line
    def scroll_to_line(self, sender, line):
        iterator = self.editor.textbuffer.get_iter_at_line(line)
        self.editor.response()
        self.editor.textbuffer.place_cursor(iterator)
        self.editor.textview.scroll_to_iter(iterator, 0.001, use_align=True, xalign=1.0)
        self.editor.response()
        return False 
    
    @signals.add
    def mark_add(self, sender, line):
        self.editor.response()
        iterator = self.editor.textbuffer.get_iter_at_line(line)
        self.editor.textbuffer.create_source_mark(None, BOOKMARK_NAME, iterator)
        self.editor.response()
        return False
    
    @signals.bookmark_lines
    def mark_lines(self, sender, lines):
        [self.mark_add(sender, line) for line in lines]
        return False    
    
    def mark_region(self, line=None):
        if line is None: return self.editor.textbuffer.get_bounds()
        start = self.editor.textbuffer.get_iter_at_line(line)
        end = self.editor.forward_to_line_end(start.copy())
        return start, end

    @signals.remove
    @signals.remove_all
    def mark_remove(self, sender, line=None):
        start, end = self.mark_region(line)
        self.editor.response()
        self.editor.textbuffer.remove_source_marks(start, end, BOOKMARK_NAME)
        self.editor.response()
        return False
    
    @signals.lines
    def margin_toggle(self, sender, lines):
        self.editor.textview.set_show_line_marks(bool(lines))
        return False
    
    @signals.lines
    def save_bookmarks(self, sender, lines):
        uri = self.editor.uri
        if not uri: return False
        self.editor.response()
        set_value(str(uri), lines)
        self.editor.response()
        return False  
    
    def restore_bookmarks(self, *args):
        uri = self.editor.uri
        if not uri: return False
        self.editor.response()
        lines = get_value(str(uri))
        self.editor.response()
        if not lines: return False
        signals.bookmark_lines.emit(lines)
        return False
    
    def unload(self):
        super(BookmarkPlugin, self).unload()
        self.mark_updater.update()
        signals.destroy.emit()
