name = "Python rope autocomplete"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
languages = ["python"]
version = 0.1
autoload = True
class_name = "PythonRopePlugin"
short_description = "Autocompletes python code"
long_description = """This plugin uses rope refactoring library
to autocomlete python code"""

import gtk
import rope.base.project
from rope.contrib import codeassist

from gettext import gettext as _
from gio import File

from scribes_helpers import Trigger, TriggerManager

trigger_complete = Trigger('activate-rope-assist', '<ctrl>space',
    'Auto complete python code', 'Python')

trigger_goto_defenition = Trigger('goto-python-definition', 'F3',
    'Navigates to definition under cursor', 'Python')


def refresh_gui():
    while gtk.events_pending():
        gtk.main_iteration_do(block=False)

class PythonRopePlugin(object):

    def __init__(self, editor):
        self.editor = editor
        self.triggers = TriggerManager(editor)
        self.triggers.connect_triggers(self)
        self.__project = None

    @property
    def project(self):
        if not self.__project:
            self.__project = rope.base.project.Project('/home/bobrov/work/scribes-goodies')
            
        return self.__project

    def load(self):
        pass

    def unload(self):
        if self.__project:
            self.__project.close()
    
    def get_source_and_offset(self):
        edit = self.editor.textbuffer
        
        cursor = edit.get_iter_at_mark(edit.get_insert())
        offset = cursor.get_offset()
        source = edit.get_text(*edit.get_bounds())
        
        return source, offset
        
    @trigger_complete(idle=False)
    def autocomplete(self, *args):
        project = self.project 
        project.validate()
                
        source, offset = self.get_source_and_offset()
        
        proposals = codeassist.code_assist(project, source, offset) 
        print [r.name for r in proposals]
        
        return False

    def goto_line(self, editor, line):
        refresh_gui()
        edit = editor.textbuffer
        iterator = edit.get_iter_at_line(line - 1)
        edit.place_cursor(iterator)
        editor.textview.scroll_to_iter(iterator, 0.001, use_align=True, xalign=1.0)
    
    @trigger_goto_defenition(idle=False)
    def goto_definition(self, *args):
        project = self.project 
        project.validate()

        try:
            resource, line = codeassist.get_definition_location(
                project, *self.get_source_and_offset())
        except Exception, e:
            print e
            return False
            
        if resource:
            uri = File(resource.real_path).get_uri()
            self.editor.open_file(uri)
            for editor in self.editor.imanager.get_editor_instances():
                if editor.uri == uri: 
                    self.goto_line(editor, line)
        else:
            if line:
                self.goto_line(self.editor, line)
            else:
                self.editor.update_message(_("Unknown definition"), "no", 1)
            
        return False
