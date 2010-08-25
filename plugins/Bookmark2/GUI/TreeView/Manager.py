class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		from Initializer import Initializer
		Initializer(manager, editor)
		from Disabler import Disabler
		Disabler(manager, editor)
		from RowSelector import Selector
		Selector(manager, editor)
#		from UpKeyHandler import Handler
#		Handler(manager, editor)
#		from KeyboardHandler import Handler
#		Handler(manager, editor)
		from RowActivationHandler import Handler
		Handler(manager, editor)
		from ModelUpdater import Updater
		Updater(manager, editor)
		from ModelDataGenerator import Generator
		Generator(manager, editor)
		editor.response()
