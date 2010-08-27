from scribes_helpers import weak_connect
from gtk.keysyms import Up, Down, Return, Escape, Left, Right
from gtk import TEXT_WINDOW_TEXT


class GUI(object):
    def __init__(self, signals, editor):
        self.signals = signals
        self.editor = editor
        self.on_select = None
        self.gui = editor.get_gui_object(globals(), 'gui.glade')
        self.gui.connect_signals(self)
        
        self.blocked = False
        self.key_press_handler_id = weak_connect(self.editor.textview,
            'key-press-event', self, 'on_key_press_event', idle=False)
        
        self.window = self.gui.get_object('window')
        self.treeview = self.gui.get_object('treeview')
        self.model = self.gui.get_object('liststore')
        self.column = self.treeview.get_column(0)
        self.selection = self.treeview.get_selection()

    def block_key_press(self):
        if not self.blocked:
            self.editor.textview.handler_block(self.key_press_handler_id)
            self.blocked = True

    def unblock_key_press(self):
        if self.blocked:
            self.editor.textview.handler_unblock(self.key_press_handler_id)
            self.blocked = False

    def show(self, on_select):
        self.move_window(200, 300)
        self.window.show()
        self.unblock_key_press()
        self.on_select = on_select
        
    def hide(self):
        self.on_select = None
        self.window.hide()
        self.block_key_press()
        
    def fill(self, proposals):
        self.treeview.set_model(None)
        self.model.clear()
        
        for p in proposals:
            self.model.append((p.name,))
            
        self.treeview.set_model(self.model)
        self.select(self.model[0])
        
    def update(self, proposals, on_select):
        self.fill(proposals)
        self.on_select = on_select
        
    def select(self, row):
        self.selection.select_iter(row.iter)
        self.treeview.set_cursor(row.path, self.column)
        self.treeview.scroll_to_cell(row.path, None, True, 0.5, 0.5)

    def select_next(self):
        model, iterator = self.selection.get_selected()
        iterator = model.iter_next(iterator)
        path = model.get_path(iterator) if iterator else 0
        self.select(model[path])

    def select_previous(self):
        model, iterator = self.selection.get_selected()
        path = model.get_path(iterator)[0] - 1
        self.select(model[path])

    def activate_selection(self):
        model, iterator = self.selection.get_selected()
        text = model.get_value(iterator, 0)
        
        if self.on_select:
            self.on_select(text)
        
        self.hide()
        
    def on_key_press_event(self, textview, event):
        if event.keyval == Escape:
            self.hide()
            return True
        elif event.keyval in (Left, Right):
            return True
        elif event.keyval == Up:
            self.select_previous()
            return True
        elif event.keyval == Down:
            self.select_next()
            return True
        elif event.keyval == Return:
            self.activate_selection()
            return True

        self.signals.text_updated.emit()        
                        
        return False

    def get_size(self, width, height):
        height = 210 if height > 200 else (height + 6)
        width = 210 if width < 200 else width
        
        return width, height

    def calculate_cords(self, width, height, cursor_data, textview_data):
        cursor_x, cursor_y, cursor_width, cursor_height = cursor_data
        textview_x, textview_y, textview_width, textview_height = textview_data
        
        position_x = textview_x + cursor_x
        if (position_x + width) <= (textview_x + textview_width):
            x = position_x
        else:
            x = (textview_x + textview_width) - width
        
        position_y = textview_y + cursor_y + cursor_height
        if (position_y + height) <= (textview_y + textview_height):
            y = position_y
        else:
            y = (textview_y + cursor_y) - height

        return x, y 

    def get_cursor_data(self):
        textview = self.editor.textview
        rectangle = textview.get_iter_location(self.editor.cursor)
        
        position = textview.buffer_to_window_coords(
            TEXT_WINDOW_TEXT, rectangle.x,rectangle.y)
        return position[0], position[1], rectangle.width, rectangle.height

    def get_textview_data(self):
        window = self.editor.textview.get_window(TEXT_WINDOW_TEXT)
        x, y = window.get_origin()
        rectangle = self.editor.textview.get_visible_rect()
        return x, y, rectangle.width, rectangle.height

    def get_cords(self, width, height):
        cursor_data = self.get_cursor_data()
        textview_data = self.get_textview_data()
        return self.calculate_cords(width, height, cursor_data, textview_data)

    def move_window(self, width, height):
        width, height = self.get_size(width, height)
        xcord, ycord = self.get_cords(width, height)
        self.window.set_size_request(width, height)
        self.window.resize(width, height)
        self.window.move(xcord, ycord)
