Disable auto-save
=================

Default auto-save policy breaks some common developing scenarios. For example:

* Hacking web application with auto code reloading feature.
* Hacking with continuous unit testing in background (``py.test --looponfail``)

This plugin turns off auto-save on timer and scribes window focus loss. So only ``<ctrl>+s`` saves your file.

