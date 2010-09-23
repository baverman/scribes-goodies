Fixed Quick Open
================

Adds very important functionality (for me) to original quick open plugin:

- Start search from project root, not from being edited file directory.

- Remembers all project roots during edit session and allows switch search between them.
  Switch by ``<alt>+Up`` in quick open dialog.

- Project roots detected automatically if project under GIT, Mercurial or Bazaar.
  Also you can manually touch ``.scribes_project`` file to mark directory as root.

- Plugin creates file ``~/.gnome2/scribes/plugins/quick_open_settings.py``
  You can insert favorite projects paths into recent_pathes list to be able switch searchable
  projects after Scribes start::

     recent_pathes = ['/home/bobrov/work/taburet', '/home/bobrov/work/scribes-goodies']
