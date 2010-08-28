Scribes Python Rope Plugin
==========================

Adds auto-complete and code navigation features to scribes editor.


Installation
------------

   pip install scribes.python.rope

Take note. During install plugin will be placed in your real home.


Using
-----

Project root is determined automatically if your code under GIT, Mercurial or Bazaar
VCSes. In other cases you should create `.ropeproject` directory manually.

After first try to autocomplete or find definition there be placed rope's `config.py` which
you may tweak.    

Shortcuts
^^^^^^^^^

`F3`: Navigate to symbol definition under cursor

`Ctrl+Space`: Performs auto-complete


TODO
----

* Use dynamic and static rope analyzing capabilities.
* Show function parameters and documentation.
* Use source code type hints.
