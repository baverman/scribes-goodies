name = "Bookmark Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>", "Anton Bobrov <bobrov@vl.ru>"]
version = 0.4
autoload = True
class_name = "BookmarkPlugin2"
short_description = "Manage bookmarked lines in a file."
long_description = """Add or remove bookmarks to lines. Navigate to 
bookmarked lines via a browser. Press ctrl+d to add or remove 
bookmarks. Press ctrl+b to navigate to bookmarked lines."""

from scribes_helpers import bootstrap

BookmarkPlugin2 = bootstrap('Bookmark2.BookmarkPlugin')
