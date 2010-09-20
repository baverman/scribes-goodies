Goto Dir
========

Default shortcut ``<crtl>+<alt>+l`` opens editor file directory in file manager.

Problems
--------

Because plugin uses ``xdg-open`` for opening directory you must
have ``mimeopen`` util installed in your system, or else directory will be
opened in Firefox.

AFAIK, debian based distributives have ``mimeopen`` from the box. For ArchLinux
you need install ``perl-file-mimeinfo`` package.
