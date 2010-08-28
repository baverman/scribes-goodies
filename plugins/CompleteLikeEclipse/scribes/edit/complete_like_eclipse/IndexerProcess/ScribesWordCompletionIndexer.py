RECURSIONLIMITMULTIPLIER = 1000

def __set_vm_properties():
	from sys import setcheckinterval, getrecursionlimit
	from sys import setrecursionlimit, setdlopenflags
	try:
		setcheckinterval(1000)
		from dl import RTLD_LAZY, RTLD_GLOBAL
		setdlopenflags(RTLD_LAZY|RTLD_GLOBAL)
	except ImportError:
		pass
	global RECURSIONLIMITMULTIPLIER
	setrecursionlimit(getrecursionlimit() * RECURSIONLIMITMULTIPLIER)
	return

if __name__ == "__main__":
	from os import nice
	nice(19)
#	__set_vm_properties()
	from sys import argv, path
	python_path = argv[1]
	path.insert(0, python_path)
	from gobject import MainLoop, threads_init
	threads_init()
	from IndexerManager import Manager
	Manager()
	MainLoop().run()
