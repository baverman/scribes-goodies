Python spec
===========

Default gtksourceview python language specification is missing some important parts:

* Style for class definition identifier
* Style for function and method definition identifier
* Default style for decorators is too noisy. Decorators are additional info without heavy
  semantic meaning, so should be appropriately styled.

This python spec tries to fix above issues.

Installing
----------

```sh
  mkdir -p ~/.local/share/gtksourceview-2.0/language-specs
  cp python.lang ~/.local/share/gtksourceview-2.0/language-specs/
