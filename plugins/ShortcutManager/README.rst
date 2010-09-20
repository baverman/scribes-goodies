Shortcut Manager
================

There is no any tool to change Scribes key bindings. All shortcuts are hard coded in python sources.
I prefer Eclipse key scheme which distinguish from standard Scribes. So I decide to write this plugin
for easy shortcut change.

Using
-----

There is menu item in standard preferences menu which activates key configuration window.
There is no any unusual things about it: `action name`, `accelerator` proper, and `action description`.
You may change accelerator by clicking on appropriate column and action or by focusing
cursor on needed item and pressing ``Enter`` key. Also, you may clear accelerator
value by pressing ``Backspace`` during editing. Thereby such action will be disabled.

Changed actions are marked by bold font. 

Closing window or pressing ``Esc`` key hides dialog and saves your key configuration.

TODO
----

* Button to reset original action accelerator value

