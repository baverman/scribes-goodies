name = "Shortcut Manager plugin"
authors = ["Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "ShortcutManagerPlugin"
short_description = "Manages shortcuts for scribes plugins"
long_description = """Allows to override hardcoded plugin trigger accelerators"""

from scribes.helpers import bootstrap

ShortcutManagerPlugin = bootstrap('scribes.editor.shortcut_manager.Plugin')
