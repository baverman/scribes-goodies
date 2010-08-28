name = "Complete word plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>", "Anton Bobrov <bobrov@vl.ru>"]
version = 0.1
autoload = True
class_name = "CompleteLikeEclipsePlugin"
short_description = "Complete word like eclipse Plugin"
long_description = """Eclipse like (Alt+/) words completer"""

from scribes.helpers import bootstrap

CompleteLikeEclipsePlugin = bootstrap('scribes.edit.complete_like_eclipse.Plugin')
