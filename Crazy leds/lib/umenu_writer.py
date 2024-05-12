try:
    from display import CENTER, RIGHT
except ImportError:
    CENTER = 1
    RIGHT = 2
from array import array
# updated Pawel Lugowski's umenu system (https://github.com/plugowski/umenu)
# with Peter Hinch's writer library and st7735r driver (https://github.com/peterhinch/micropython-font-to-py)
# writer library allows rendering text to a monochrome or colour display having a suitable device driver
# used TFT 1,8' (160x128) display
from gui.core.writer import CWriter

def menu_parameters(display, writer, x0, y0, line_height, m_width, per_page, v_padding):  
    # format: self.display, self.writer,self.x0,self.y0,self.line_height,self.m_width,self.per_page,self.v_padding)
    global m_params
    m_params = [display, writer, x0, y0, line_height, m_width, per_page, v_padding]

def active_item_v_pos(y_v_padding):
    # cross method for passing active item vertical position
    global a_i_value
    a_i_value = y_v_padding

# Convert r, g, b in range 0-255 to an 8 bit colour value
# rrrgggbb. Converted to 12 bit on the fly.

def rgb2rgb444(color):
    r,g,b = color
    return (r & 0xe0) | ((g >> 3) & 0x1c) | (b >> 6)

class MenuItem():

    def __init__(self, name: str, decorator=None, visible=None):
        self.parent = None
        self._visible = True if visible is None else visible
        self._callback = None
        self.is_active = False
        self.name = name
        self.decorator = '' if decorator is None else decorator

    @property
    def visible(self):
        return self._visible if not self._check_callable(self._visible, False) else self._call_callable(self._visible)

    def click(self):
        raise NotImplementedError()

    def get_decorator(self):
        return self.decorator if not callable(self.decorator) else self.decorator()

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, callback):
        self._check_callable(callback)
        self._callback = callback

    @staticmethod
    def _check_callable(param, raise_error=True):
        if not (callable(param) or (type(param) is tuple and callable(param[0]))):
            if raise_error:
                raise ValueError('callable param should be callable or tuple with callable on first place!')
            else:
                return False
        return True

    @staticmethod
    def _call_callable(func, *args):
        if callable(func):
            return func(*args)
        elif type(func) is tuple and callable(func[0]):
            in_args = func[1] if type(func[1]) is tuple else (func[1],)
            return func[0](*tuple(list(in_args) + list(args)))


class SubMenuItem(MenuItem):
    menu = None

    def __init__(self, name, decorator=None, visible=None):
        super().__init__(name, '>' if decorator is None else decorator, visible)
        self.menu = MenuScreen(name, None)

    def click(self):
        pass

    def add(self, item, parent=None) -> 'SubMenuItem':
        self.menu.add(item, parent)
        return self

    def reset(self):
        self.menu.reset()


class CallbackItem(MenuItem):

    def __init__(self, name, callback, decorator=None, return_parent=True, visible=None):
        super().__init__(name, decorator, visible)
        self.callback = callback
        self.return_parent = return_parent

    def click(self):
        self._call_callable(self.callback)
        if self.return_parent:
            return self.parent


class ToggleItem(CallbackItem):

    def __init__(self, name, state_callback, change_callback, visible=None):
        super().__init__(name, change_callback, visible=visible)
        self._check_callable(state_callback)
        self.state_callback = state_callback

    def check_status(self):
        return self._call_callable(self.state_callback)

    def get_decorator(self):
        return '[x]' if self.check_status() else '[ ]'


class ConfirmItem(SubMenuItem):

    def __init__(self, name, callback, question=None, answers=None, decorator='', visible=None):
        super().__init__(name, decorator, visible=visible)
        self.callback = callback
        self._question = question if question is not None else 'Are you sure?'
        self._answers = answers if answers is not None else ('yes', 'no')

    def click(self):
        self.reset()
        self.menu.title = self._question

        for pos in range(len(self._answers)):
            name = self._answers[pos]
            self.add(CallbackItem(name, self.callback if pos == 0 else lambda: True), self.parent)

        return self.menu


class EnumItem(SubMenuItem):

    def __init__(self, name, items, callback, selected=None, visible=None):
        super().__init__(name, visible=visible)
        if not isinstance(items, list):
            raise ValueError("items should be a list!")
        self.callback = callback
        self.items = items
        self.selected = 0 if selected is None else self._get_index_by_key(selected)

        self._set_decorator()

    def choose(self, selection):
        self.selected = selection
        self._set_decorator()
        self._call_callable(self.callback, self._get_element()[0])

    def click(self):
        self.reset()
        for pos in range(len(self.items)):
            if isinstance(self.items[pos], dict):
                name = self.items[pos]['name']
            else:
                name = self.items[pos]
            decorator = '<<' if pos == self.selected else ''
            self.add(CallbackItem(name, (self.choose, pos), decorator), self.parent)

        return self.menu

    def _get_index_by_key(self, key):

        if 'value' not in self.items[0]:
            if type(key) is int:
                return key

        i = 0
        for item in self.items:
            if ('value' in item and item['value'] == key) or item['name'] == key:
                return i
            i += 1
        raise ValueError('No index for key: {}!'.format(key))

    def _get_element(self):
        if isinstance(self.items[self.selected], str):
            return self.items[self.selected], self.items[self.selected]

        # noinspection PyTypeChecker
        return self.items[self.selected]['value'], self.items[self.selected]['name']

    def _set_decorator(self):
        self.decorator = self._get_element()[1]


class InfoItem(MenuItem):

    def __init__(self, name, decorator='', visible=None):
        super().__init__(name, decorator, visible=visible)

    def click(self):
        return self.parent


class CustomItem(MenuItem):

    def __init__(self, name, visible=None):
        super().__init__(name, visible=visible)
        self.display = None  # it is set after initialization via Menu._update_display()

    def click(self):
        return self

    def up(self):
        # called when menu.move(-1) is called
        pass

    def down(self):
        # called when menu.move(1) is called
        pass

    def select(self):
        # called when menu.click() is called (on button press)
        # should return Instance of MenuItem (usually self.parent - if want to go level up or self to stay in current context)
        raise NotImplementedError()

    def draw(self):
        # called when someone click on menu item
        raise NotImplementedError()


class ValueItem(CustomItem, CallbackItem):

    def __init__(self, name, value_reader, min_v, max_v, step, callback, visible=None):
        super().__init__(name, visible=visible)
        self._value = value_reader if not self._check_callable(value_reader, False) else 0
        self.value_reader = value_reader
        self.min_v = min_v
        self.max_v = max_v
        self.step = step
        self.precision = 0 if '.' not in str(step) else len(str(step).split('.')[1])
        self.callback = callback

    def draw(self):
        
        '''self.display.aled_fill(0)
        if hasattr(self.display, 'rich_text'):
            self.display.text(str.upper(self.name), None, 0, 1, align=CENTER)
            self.display.rich_text(str(self.value), None, 20, 1, size=5, align=CENTER)
        else:
            x_pos = self.display.width - (len(self.name) * 8) - 1
            self.display.text(str.upper(self.name), x_pos, 0, 1)
            x_pos = self.display.width - (len(str(self.value)) * 8) - 1
            self.display.text(str(self.value), x_pos, 20, 1)

        #self.display.hline(0, 10, self.display.width, 1)
        '''
        #               0        1    2   3      4           5        6          7 
        #m_params = [display, writer,x0, y0, line_height, m_width, per_page, v_padding]
        #                        
        #a_i_value = y_v_padding
        
        x = m_params[2]+m_params[5]        
        m_params[0].fill_rect(x-25,a_i_value-m_params[7], x-m_params[2]-6, m_params[4], m_params[1].fgcolor)
        m_params[1].set_textpos(m_params[0],a_i_value, x-22)
        m_params[1].printstring(self.get_decorator(), 1)
        #print('x-10:     ', x) # debug purposes only
        self.display.show()

    def select(self):
        return self.parent

    def up(self):
        if self.value < self.max_v:
            v = self.value + self.step
            self.value = int(v) if self.precision == 0 else round(v, self.precision)
        self.draw()

    def down(self):
        if self.value > self.min_v:
            v = self.value - self.step
            self.value = int(v) if self.precision == 0 else round(v, self.precision)
        self.draw()

    @property
    def value(self):
        return self._value \
            if not self._check_callable(self.value_reader, False) \
            else self._call_callable(self.value_reader)

    @value.setter
    def value(self, value):
        self._value = value
        self._call_callable(self.callback, self._value)

    def get_decorator(self):
        return str(self.value)

class BackItem(MenuItem):

    def __init__(self, parent, label='< BACK'):
        super().__init__(label)
        self.parent = parent

    def click(self):
        return self.parent


class ExitItem(MenuItem):

    def __init__(self, parent, label='^ EXIT'):
        super().__init__(label)
        self.parent = parent

    def click(self):
        self.reset()


class MenuScreen:

    def __init__(self, title: str, parent=None):
        self._items = []
        self._visible_items = []
        self.selected = 0
        self.parent = parent
        self.title = title

    def add(self, item, parent=None):
        item.parent = self if parent is None else parent
        if type(item) is SubMenuItem:
            item.menu.parent = self if parent is None else parent
        self._items.append(item)
        return self

    def reset(self):
        self._items = []

    def count(self) -> int:
        elements = 0
        self._visible_items = []
        for item in self._items:
            if item.visible:
                elements += 1
                self._visible_items.append(item)
        return elements + (1 if self.parent is not None else 0)

    def up(self) -> None:
        if self.selected > 0:
            self.selected = self.selected - 1

    def down(self) -> None:
        if self.selected + 1 < self.count():
            self.selected = self.selected + 1

    def get(self, position):

        if position < 0 or position + 1 > self.count():
            return None

        if position + 1 == self.count() and self.parent is not None:
            item = BackItem(self.parent)
        else:
            item = self._visible_items[position]

        item.is_active = position == self.selected
        return item

    def select(self) -> None:

        item = self.get(self.selected)
        if type(item) is BackItem:
            self.selected = 0

        if type(item) is SubMenuItem:
            return item.menu
        else:
            # do action and return current menu
            return item.click()


class Menu:
    current_screen = None  # type: MenuScreen | CustomItem

    def __init__(self, display,writer,per_page: int = 4, line_height: int = 0, x0: int = 0, y0: int = 0, m_width: int = None, menu_header=True):

        self.display = display  # display driver
        self.writer = writer  # CWriter(display,font, self.fgcolor,self.bgcolor,verbose=True)
        self.writer.set_clip(True, True, False)
        # colors defined in writer
        self.fgcolor = self.writer.fgcolor
        self.bgcolor = self.writer.bgcolor
        self.menu_header = menu_header
        # menu screen coordinates and sizes
        self.x0 = x0
        self.y0 = y0
        if m_width == None:
            self.m_width = self.display.width
        else:
            self.m_width = m_width
        self.font_height = self.writer.font.height()
        self.font_width = self.writer.font.max_width()

        self.line_height = self.font_height + 4
        if line_height > 0:
            self.line_height = line_height
        self.v_padding = int((self.line_height - self.font_height) / 2)
        self.per_page = per_page

        self.main_screen = None
        self.set_globals()

    def set_globals(self):
        menu_parameters(self.display, self.writer,self.x0,self.y0,self.line_height,self.m_width,self.per_page,self.v_padding)
        
    def set_screen(self, screen: MenuScreen):
        self.current_screen = screen
        if self.main_screen is None:
            self.main_screen = screen
            self._update_display(screen._items)

    def move(self, direction: int = 1):
        self.current_screen.up() if direction < 0 else self.current_screen.down()
        self.draw()

    def click(self):
        self.current_screen = self.current_screen.select()
        if self.current_screen is not None:
            self.draw()

    def reset(self):
        self.current_screen = self.main_screen
        self.current_screen.selected = 0
        self.draw()

    def draw(self):

        if type(self.current_screen) is not MenuScreen:
            self.current_screen.draw()
            return

        self.display.fill(0)
        if self.menu_header: self._menu_header(self.current_screen.title)

        elements = self.current_screen.count()
        start = self.current_screen.selected - self.per_page + 1 if self.current_screen.selected + 1 > self.per_page else 0
        end = start + self.per_page
        
        
        menu_pos = 0
        for i in range(start, end if end < elements else elements):
            self._item_line(self.current_screen.get(i), menu_pos)
            menu_pos += 1

        self.display.show()

    def set_font(self, font):
        self.font = font
        self.writer.font = self.font
        self.font_height = self.writer.font.height()
        self.font_width = self.writer.font.max_width()

    def set_origin(self, x0, y0):
        self.x0 = x0
        self.y0 = y0
        self.writer.set_textpos(self.display, self.y0, self.x0)
        self.set_globals()

    def set_colors(self, fgcolor, bgcolor):
        # colors have to be passed in rgb555 format
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.writer.setcolor(self.fgcolor, self.bgcolor)

    def set_line_height(self, line_height):
        self.line_height = line_height
        self.set_globals()

    def set_per_page(self, per_page):
        self.per_page = per_page
        self.set_globals()

    def _item_line(self, item: MenuItem, pos):
        if self.menu_header:
            menu_y_end = self.line_height
        else:
            menu_y_end = 0
        y = self.y0 + menu_y_end + (pos * self.line_height)
        v_padding = int((self.line_height - self.font_height) / 2)
        y_v_padding = y + v_padding
        if item.is_active:
            background = self.fgcolor
            active_item_v_pos(y_v_padding) # a_i_value method format: y_v_padding
        else:
            background = self.bgcolor
        self.display.fill_rect(self.x0, y, self.m_width, self.line_height, background)
        x_pos = self.m_width - self.writer.stringlen(item.get_decorator())-2
        x0_x_pos = self.x0 + x_pos
        #Label(self.writer, self.y0 + y + v_padding,self.x0 + 2 , str.upper(item.name),invert = item.is_active, align=0)
        #Label(self.writer, self.y0 + y + v_padding, self.x0 + x_pos, str.upper(item.get_decorator()),invert = item.is_active, align=1)
        # item name
        self.writer.set_textpos(self.display, y_v_padding,self.x0 + 1)
        self.writer.printstring(item.name, item.is_active)
        # value or decorator
        self.writer.set_textpos(self.display, y_v_padding, x0_x_pos)
        self.writer.printstring(item.get_decorator(), item.is_active)        
        
    def _menu_header(self, text):
        x = int((self.m_width / 2) - (self.writer.stringlen(text) / 2))
        self.writer.set_textpos(self.display, self.y0, self.x0 + x)
        self.writer.printstring(str.upper(self.current_screen.title), 0)
        self.display.hline(self.x0, self.y0 + self.font_height + 2, self.m_width, self.fgcolor)

    def not_background(self,background):
        if background == self.bgcolor:
            return self.fgcolor
        else:
            return self.bgcolor

    def _update_display(self, menu_items):
        """
        Add display object to all CustomItems, as it can be useful there to draw custom screens
        """
        for obj in menu_items:
            if isinstance(obj, CustomItem):
                obj.display = self.display
            if isinstance(obj, SubMenuItem):
                self._update_display(obj.menu._items)
