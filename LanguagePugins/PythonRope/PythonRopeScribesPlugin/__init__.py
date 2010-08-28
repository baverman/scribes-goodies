import gtk
import traceback
import rope.base.project
from rope.contrib import codeassist
from rope.base import libutils

from gettext import gettext as _
from gio import File

from scribes_helpers import Trigger, TriggerManager, Signal, SignalManager

from gui import GUI

trigger_complete = Trigger('activate-rope-assist', '<ctrl>space',
    'Auto complete python code', 'Python')

trigger_goto_definition = Trigger('goto-python-definition', 'F3',
    'Navigates to definition under cursor', 'Python')


def refresh_gui():
    while gtk.events_pending():
        gtk.main_iteration_do(block=False)

def find_project_root(uri):
    f = File(uri)
    special_names = ('.ropeproject', '.git', '.hg', '.bzr', '.scribes_project')
    while True:
        for name in special_names:
            if f.get_child(name).query_exists():
                return f.get_path()
        
        p = f.get_parent()
        if p:
            f = p
        else:
            return None


class Signals(SignalManager):
    text_updated = Signal()


class Plugin(object):

    def __init__(self, editor):
        self.editor = editor
        self.triggers = TriggerManager(editor)
        self.triggers.connect_triggers(self)
        
        self.signals = Signals()
        self.signals.connect_signals(self)

    @property
    def project(self):
        try:
            return self.__project
        except AttributeError:
            root = find_project_root(self.editor.pwd_uri)
            if root:
                self.__project = rope.base.project.Project(root)
            else:
                self.__project = None
                
            return self.__project

    @property
    def gui(self):
        try:
            return self.__gui
        except AttributeError:
            self.__gui = GUI(self.signals, self.editor)
            return self.__gui 

    def unload(self):
        if getattr(self, '__project', None):
            self.__project.close()

    def get_rope_resource(self, project):    
        return libutils.path_to_resource(project, File(self.editor.uri).get_path())
        
    def get_source_and_offset(self):
        edit = self.editor.textbuffer
        
        cursor = edit.get_iter_at_mark(edit.get_insert())
        offset = cursor.get_offset()
        source = edit.get_text(*edit.get_bounds())
        
        if not isinstance(source, unicode):
            source = source.decode('utf8')
        
        return source, offset
    
    @Signals.text_updated(idle=True)
    def text_updated(self, *args):
        refresh_gui()
        self.update_proposals(True)
        return False
    
    def update_proposals(self, update):
        source, offset = self.get_source_and_offset()
        
        try:
            proposals = codeassist.sorted_proposals(
                codeassist.code_assist(self.project, source, offset,
                    resource=self.get_rope_resource(self.project)))
        except Exception, e:
            self.editor.update_message(str(e), "no", 1)
            traceback.print_exc() 
            return False
            
        
        def on_select(proposal):
            self.gui.hide()

            edit = self.editor.textbuffer
            start_offset = codeassist.starting_offset(source, offset)

            start = edit.get_iter_at_offset(start_offset)
            end = self.editor.cursor

            edit.delete(start, end)
            edit.insert(start, proposal)
        
        if len(proposals) > 1:
            if update:
                self.gui.update(proposals, on_select)
            else:
                self.gui.fill(proposals)
                self.gui.show(on_select)
        elif len(proposals) == 1:
            on_select(proposals[0].name)
        else:
            self.editor.update_message(_("No assist"), "no", 1)
        
    @trigger_complete
    def autocomplete(self, *args):
        project = self.project 
        if not project:
            self.editor.update_message(_("Can't find project path"), "no", 1)
            return False

        project.validate()
        
        self.update_proposals(False)
        
        return False

    def goto_line(self, editor, line):
        refresh_gui()
        edit = editor.textbuffer
        iterator = edit.get_iter_at_line(line - 1)
        edit.place_cursor(iterator)
        editor.textview.scroll_to_iter(iterator, 0.001, use_align=True, xalign=1.0)
    
    @trigger_goto_definition
    def goto_definition(self, *args):
        project = self.project
        if not project:
            project = getattr(self.editor, 'ropeproject', None)
            if not project:
                self.editor.update_message(_("Can't find project path"), "no", 1)
                return False
         
        project.validate()
        
        current_resource = self.get_rope_resource(project) 
        
        try:
            resource, line = codeassist.get_definition_location(
                project, *self.get_source_and_offset(),
                resource=current_resource)
        except Exception, e:
            self.editor.update_message(str(e), "no", 1)
            traceback.print_exc()
            return False
        
        if resource.real_path == current_resource.real_path:
            resource = None
            
        if resource:
            uri = File(resource.real_path).get_uri()
            self.editor.open_file(uri)
            for editor in self.editor.imanager.get_editor_instances():
                if editor.uri == uri: 
                    editor.ropeproject = project 
                    self.goto_line(editor, line)
        else:
            if line:
                self.goto_line(self.editor, line)
            else:
                self.editor.update_message(_("Unknown definition"), "no", 1)
            
        return False
