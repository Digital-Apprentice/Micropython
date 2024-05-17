#from cl_main_classes import Controller
from machine import Timer



from umenu_writer import * # updated Pawel Lugowski's umenu system to use Peter Hinch's nanogui library
#from gui.core.writer import CWriter, circle, fillcircle, clip_rect, fill_clip_rect, draw_circle_segment
#import fonts for the menu
import uasyncio as asyncio
#from cl_palettes import red, green, blue, yellow, cyan, magenta, purple, orange, pink, darkslategray, darkgreen, darkblue, darkred, darkorange, darkmagenta, darkcyan, darkviolet, darkyellow, darkyellow2, white, black
from cl_palettes import full_saturation_spectrum as fss
#import gui.fonts.freesans20 as freesans20
#import gui.fonts.font10 as font10
#import gui.fonts.font6 as font6
#import gui.fonts.nrg30 as nrg30
#import gui.fonts.nrg26 as nrg26
#import gui.fonts.nrg24 as nrg24
#import gui.fonts.nrg22 as nrg22
#import gui.fonts.nrg20 as nrg20
#import gui.fonts.nrg18 as nrg18
#import gui.fonts.nrg16 as nrg16
#import gui.fonts.nrg14 as nrg14
#import gui.fonts.nrg12 as nrg12
#import gui.fonts.nrg10 as nrg10

#import gui.fonts.arial10 as arial10

#import gui.fonts.TTOTCL10 as TTOTCL10

#import gui.fonts.TTOTCoL10 as TTOTCoL10
#import gui.fonts.TTOTM10 as TTOTM10
#import gui.fonts.TTOTDB16 as TTOTDB16
#import gui.fonts.TTOTDB20 as TTOTDB20
#wr_menu = CWriter(c.display, arial10, fgcolor=c.display.rgb(darkyellow), bgcolor=c.display.rgb(black), verbose=False)
#wr_dashb = CWriter(c.display, nrg20, fgcolor=c.display.rgb(white), bgcolor=c.display.rgb(black), verbose=False)


#display,writer,per_page: int = 4, line_height: int = 0, x0: int = 0, y0: int = 0, m_width: int = None, menu_header=True)



'''
class MenuScreen:

    def __init__(self, title: str, width: int, parent=None, x0=0, y0=0 ):
        self._items = []
        self._visible_items = []
        self.selected = 0
        self.parent = parent
        self.title = title

        self.x = x0
        self.y = y0
        self.width = width
        self.cp_left = self._center_point(self.x, width)
        self.cp_right = self._center_point(width, c.display.width)
        self.padding = 2
        self.draw_default()

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

    def draw_default(self):
        c.display.fill(0)
        self.clock()
        self.date()
        self.sensor()
        c.display.show()

    def clock(self):
        wr_dashb.font = nrg20
        wr_dashb.setcolor(c.display.rgb(white), c.display.rgb(black))
        clock = c.get_time()
        half_len = 43
        x = self.cp_left - half_len
        for idx, t in enumerate(clock):
            for n in t:
                if int(n) == 1:
                    wr_dashb.set_textpos(c.display, x + 3, self.y + self.padding)
                else:
                    wr_dashb.set_textpos(c.display, x, self.y + self.padding)
                wr_dashb.printstring(n)
                x += 13
            wr_dashb.set_textpos(c.display, x + 1, self.y + self.padding)
            if idx < 2: wr_dashb.printstring(':')
            x += 6
        self.clock_height = wr_dashb.font.height()
        c.display.hline(self.cp_left - half_len, self.clock_height, 2 * half_len + 6, c.display.rgb(fss[int(50)]))
        self.clock_height += self.padding

    def date(self):
        wr_dashb.font = arial10
        wr_dashb.fgcolor = c.display.rgb(cyan)
        wr_dashb.bgcolor = c.display.rgb(black)
        d, m, y, w = c.get_date()
        date_str = w + '  ' + d + '.' + m + '.' + y
        date_str_len = wr_dashb.stringlen(date_str)
        x = self.cp_left - date_str_len // 2 + 3
        y = self.y + self.clock_height
        wr_dashb.set_textpos(c.display, x, y + self.padding)
        wr_dashb.printstring(date_str)
        self.date_height = wr_dashb.font.height() + self.padding

    def sensor(self):
        font = (nrg10, nrg14, nrg20)
        fg_color = c.display.rgb(white)
        bg_color = c.display.rgb(black)
        wr_dashb.setcolor(fg_color, bg_color)
        x = self.width
        y = self.y + 8
        wr_dashb.font = font[2]
        y_padding = (wr_dashb.font.height() + 12)
        w = wr_dashb.font.max_width() * 3 + self.padding
        h = wr_dashb.font.height() + self.padding
        r = (wr_dashb.font.height() + 3) // 2
        s = ('T', 'H', 'P')
        j = ('°C', '%', 'hPa')
        for idx, d in enumerate((c.temperature, c.humidity, c.pressure)):
            if idx == 0:
                v = (43 - int(d)) % 100
            elif idx == 1:
                v = int(d) % 100
            else:
                v = (int(d) - 920) % 100
            if d > 56:
                fg_color = c.display.rgb(white)
            else:
                fg_color = c.display.rgb(black)
            bg_color = c.display.rgb(fss[int(v)])
            c.display.rect(self.cp_right - 14, y + idx * y_padding, w, h, bg_color, True)
            fillcircle(c.display, self.cp_right - 14, y + idx * y_padding + 4, r, c.display.rgb(black))
            wr_dashb.font = font[2]
            wr_dashb.setcolor(c.display.rgb(white), c.display.rgb(black))
            wr_dashb.set_textpos(c.display, self.cp_right - 24, y + idx * y_padding - 6)
            wr_dashb.printstring(s[idx])
            wr_dashb.font = font[1]
            wr_dashb.setcolor(fg_color, bg_color)
            wr_dashb.set_textpos(c.display, self.cp_right - 2, y + idx * y_padding + 5)
            wr_dashb.printstring(str(d))
            wr_dashb.font = font[0]
            wr_dashb.setcolor(c.display.rgb(white), c.display.rgb(black))
            wr_dashb.set_textpos(c.display, self.cp_right - 24, y + idx * y_padding + 14)
            wr_dashb.printstring(j[idx])

    def _center_point(self, x=0, width=c.display.width):
        return  (width - x) // 2 + x
'''

def change_color(arg):
    menu.set_colors(c.display.rgb(fss[arg]),c.display.rgb(black))

menu = Menu(c.display, per_page= 5,line_height=12,x0=0,y0=36,yds=0, m_width=90,menu_header=True)
menu.set_screen(MenuScreen('MENU')
            .add(ValueItem('Color menu', 5, 0, len(fss)-1, 1, change_color,1))
            .add(ConfirmItem("Print XXX", (print, 'XXX'), "Do that?", ('yeah, sure!', 'nah, sorry!')))
            .add(InfoItem('LED1:', str(c.led1.led_active)))
            .add(InfoItem('LED2:', str(c.led2.led_active)))
            )
menu.draw()


async def switch_handler():
    r = c.encoder
    while True:
        if c.display_refresh:  # display refresh is needed
            #print(c.hour,c.minutes,c.seconds,c.year,c.month,c.day,c.weekday)
            #print(c.temperature,c.humidity,c.pressure)
            c.display_refresh = False
            menu.draw()
            
        if r.value() != 0:
            menu.move(r.value())
            r.value(0)
            c.beep(1)
        if r.state_value() != 0:
            menu.click()
            r.clear_button_state()
            c.beep()
        asyncio.sleep_ms(80)


asyncio.run(switch_handler())
'''
  
class DefaultScreen(CustomItem):
    def __init__(self, name, width,x0=0, y0=0):
        super().__init__(name)
        self.x = x0
        self.y = y0
        self.width = width
        self.cp_left = self._center_point(self.x, width)
        self.cp_right = self._center_point(width, c.display.width)

        self.padding = 2

        self.draw_default()

    def up(self):
        pass
        #self.menu.move(-1)

    def down(self):
        pass
        #self.menu.move()

    def select(self):
        #menu.click()
        return self

    def draw_default(self):
        c.display.fill(0)
        self.clock()
        self.date()
        self.sensor()
        c.display.show()


    def clock(self):
        wr_dashb.font = nrg20
        wr_dashb.setcolor(c.display.rgb(white), c.display.rgb(black))
        clock = c.get_time()
        half_len = 43
        x = self.cp_left - half_len
        for idx,t in enumerate(clock):
            for n in t:
                if int(n) == 1:
                    wr_dashb.set_textpos(c.display, x+3, self.y + self.padding)
                else:
                    wr_dashb.set_textpos(c.display, x, self.y + self.padding)
                wr_dashb.printstring(n)
                x += 13
            wr_dashb.set_textpos(c.display, x+1, self.y + self.padding)
            if idx < 2: wr_dashb.printstring(':')
            x += 6
        self.clock_height = wr_dashb.font.height()
        c.display.hline(self.cp_left - half_len, self.clock_height, 2 * half_len+6, c.display.rgb(fss[int(50)]))
        self.clock_height += self.padding

    def date(self):
        wr_dashb.font = arial10
        wr_dashb.fgcolor = c.display.rgb(cyan)
        wr_dashb.bgcolor = c.display.rgb(black)
        d, m, y, w = c.get_date()
        date_str = w + '  ' + d + '.' + m + '.' + y
        date_str_len = wr_dashb.stringlen(date_str)
        x = self.cp_left - date_str_len // 2 + 3
        y = self.y + self.clock_height
        wr_dashb.set_textpos(c.display, x, y + self.padding)
        wr_dashb.printstring(date_str)
        self.date_height = wr_dashb.font.height() + self.padding

    def sensor(self):
        font = (nrg10, nrg14, nrg20)
        fg_color = c.display.rgb(white)
        bg_color = c.display.rgb(black)
        wr_dashb.setcolor(fg_color,bg_color)
        x = self.width
        y = self.y+8
        wr_dashb.font = font[2]
        y_padding = (wr_dashb.font.height() + 12)
        w = wr_dashb.font.max_width()*3+self.padding
        h = wr_dashb.font.height()+ self.padding
        r = (wr_dashb.font.height()+3)//2
        s = ('T','H','P')
        j = ('°C', '%', 'hPa')
        for idx, d in enumerate((c.temperature, c.humidity, c.pressure)):
            if idx == 0:
                v = (43 - int(d)) % 100
            elif idx == 1:
                v = int(d)  % 100
            else:
                v = (int(d) - 920) % 100
            if d > 56:
                fg_color = c.display.rgb(white)
            else:
                fg_color = c.display.rgb(black)
            bg_color = c.display.rgb(fss[int(v)])
            c.display.rect(self.cp_right-14,y+idx*y_padding, w, h, bg_color,True)
            fillcircle(c.display, self.cp_right-14, y+idx*y_padding+4, r, c.display.rgb(black))
            wr_dashb.font = font[2]
            wr_dashb.setcolor(c.display.rgb(white), c.display.rgb(black))
            wr_dashb.set_textpos(c.display, self.cp_right-24, y+idx*y_padding-6)
            wr_dashb.printstring(s[idx])
            wr_dashb.font = font[1]
            wr_dashb.setcolor(fg_color, bg_color)
            wr_dashb.set_textpos(c.display, self.cp_right-2, y + idx * y_padding + 5)
            wr_dashb.printstring(str(d))
            wr_dashb.font = font[0]
            wr_dashb.setcolor(c.display.rgb(white), c.display.rgb(black))
            wr_dashb.set_textpos(c.display, self.cp_right - 24, y + idx * y_padding +14)
            wr_dashb.printstring(j[idx])

    def _center_point(self, x=0, width=c.display.width):
        xc = (width - x) // 2 + x
        return xc

class DefaultScreen1(MenuScreen):
    def __init__(self, name):
        super().__init__(name)
        self.x = 0
        self.y = 0
        self.cp = self._center_point()
        self.padding = 2
        self.draw_default()
   
    def up(self):
        pass
        #self.menu.move(-1)

    def down(self):
        pass
        #self.menu.move()

    def select(self):
        #self._menu.click()
        return self

    def draw_default(self):
        c.display.fill(0)
        self.clock()
        self.date()
        self.sensor()
        c.display.show()

    def draw(self):
        pass
        #self.draw_default()

    def clock(self):
        wr_dashb.font = nrg20
        wr_dashb.setcolor(c.display.rgb(darkslategray), c.display.rgb(black))
        clock = c.get_time()
        half_len = 43
        x = self.cp - half_len
        for idx,t in enumerate(clock):
            for n in t:
                if int(n) == 1:
                    wr_dashb.set_textpos(c.display, x+3, self.y + self.padding)
                else:
                    wr_dashb.set_textpos(c.display, x, self.y + self.padding)
                wr_dashb.printstring(n)
                x += 12
            wr_dashb.set_textpos(c.display, x+2, self.y + self.padding)
            if idx < 2: wr_dashb.printstring(':')
            x += 6
        self.clock_height = wr_dashb.font.height()
        c.display.hline(self.cp - half_len, self.clock_height, 2*half_len, c.display.rgb(fss[int(50)]))
        self.clock_height += self.padding

    def date(self):
        wr_dashb.font = arial10
        wr_dashb.setcolor(c.display.rgb(cyan), c.display.rgb(black))
        d, m, y, w = c.get_date()
        date_str = w + '  ' + d + '.' + m + '.' + y
        date_str_len = wr_dashb.stringlen(date_str)
        x = self.cp-date_str_len//2
        y = self.y + self.clock_height
        wr_dashb.set_textpos(c.display, x, y + self.padding)
        wr_dashb.printstring(date_str)
        self.date_height = wr_dashb.font.height()+self.padding

    def sensor(self):
        wr_dashb.font = nrg10
        wr_dashb.setcolor(c.display.rgb(darkslategray), c.display.rgb(black))
        t_str = 'T: ' + str(c.temperature) + '  °C'
        h_str = 'H: ' + str(c.humidity) + '  %'
        p_str = 'P: ' + str(c.pressure) + ' hPa'
        bg_color = c.display.rgb(fss[int(c.humidity)])
        if c.humidity > 56:
            fg_color = c.display.rgb(white)
        else:
            fg_color = c.display.rgb(black)
        x = self.cp-33
        y = self.y + self.clock_height + self.date_height
        fill_clip_rect(c.display, x-5 , y, 70 + 4*self.padding, 3 * wr_dashb.font.height() + self.padding,bg_color)
        wr_dashb.setcolor(fg_color,bg_color)
        for idx,data in enumerate ((t_str,h_str,p_str)):
            wr_dashb.set_textpos(c.display, x, y + idx*wr_dashb.font.height()+self.padding)
            wr_dashb.printstring(data)
            #if idx < 2: c.display.hline(x,  y + (idx+1) * wr_dashb.font.height()+self.padding//2, 54, c.display.rgb(white))
            #print(y + idx * wr_dashb.font.height() + self.padding)
        #print('3',y + 3 * wr_dashb.font.height() + self.padding)
        #self.sensor_height = wr_dashb.font.height()+self.padding

    def _center_point(self,width=c.display.width):
        xc = (width - self.x) // 2
        return xc



class DrawCustomScreen(CustomItem):

    def __init__(self, name):
        super().__init__(name)

    def select(self):
        return self.parent  # this is needed to go back to previous view when SET button is pushed

    def draw(self):
        c.display.fill(0)
        c.display.rect(0, 0, c.display.width, c.display.height, c.display.rgb(magenta))
        c.display.text('inny tekst', 0, 10, c.display.rgb(darkred))
        c.display.hline(0, 32, c.display.width, c.display.rgb(magenta))
        c.display.show()




#########################################

class Menu(object):
    
    def __init__(self, name, top=None, btm=None, sub=None, eff=None, param=None):
        self.menu_type = name                  # name of the menu
        self.item_highlighted = None
        self.item_selected = None           # current selected item - which item is chosen
        #self.item_previous = None          # previous item - used in the menu screen to draw the item before the selected one
        #self.item_next = None              # next item - used in the menu screen to draw next item after the selected one
        self.active = False                 # is the menu active
        self.menu_level_no = 0              # menu level - deepness of the menu, 0 is the default menu
        self.btm_no = btm                   # bottom menu number
        self.top_no = top                   # top menu number
        self.sub_no = sub                   # type of effects - number of submenu
        self.effect_type = eff                # number of the effect
        self.param_no = param               # parameter level - deepness of the parameter, 0 is the default parameter
        self.effect_selected= 0             # selected effect
        self.params_list_selected = 0       # selected list of parameters
        self.params_set = 0                 # selected set of parameters

    def get_menu(self,menu_type, menu_no):
        # menu types: btm - bottom menu, top - top menu, sub - submenu, eff - effects, param - parameters, color - colors
        if menu_type == 'btm':
            return self.bottom_menu(menu_no)
        elif menu_type == 'top':
            return self.top_menu(menu_no)
        elif menu_type == 'sub':
            return self.sub_menu(menu_no)
        elif menu_type == 'eff':
            return self.effects_menu(menu_no)
        elif menu_type == 'param':
            return self.param_menu(menu_no)
        elif menu_type == 'color':
            return self.color_menu()



    def bottom_menu(self,btm_no):
        btm_menu = [['Effects','Elephants','TLines','Settings'],['','+1','+10','Back'],['Auto','Manual','','Back']]
        self.btm_no = btm_no
        return btm_menu[self.btm_no], len(btm_menu[self.btm_no])

    def top_menu(self,top_no):
        top_menu = ['Brightness','Clock ThreeLines',]
        self.top_no = top_no
        return top_menu[self.top_no], len(top_menu[self.top_no])

    def sub_menu(self, sub_no):
        sub_menu = ['Light Effects','Gravity Effects','Sound Effects','Physical Effects']
        self.sub_no = sub_no
        return sub_menu[self.sub_no], len(sub_menu[self.sub_no])

    def effects_menu(self, effect_type):

        light_eff = ['Solid','Rainbow','Comet','Storm','Sparks','Madelaine','Mixer','Heartbeat']
        gravity_eff = ['Springs','Pong','Pendulum','Rolling stones','Rain','Snow','Particles','Sandglass']
        sound_eff = ['Spectrum','VU Meter','Sound Waves','Sound Particles','Sound Rush']
        physical_eff = ['Clock','Sensors data','All together','Temperature','Humidity','Pressure']
        effects = (light_eff,gravity_eff,sound_eff,physical_eff)
        self.effect_type = effect_type
        return effects[effect_type], len(effects[effect_type])

    #@staticmethod
    #def param_menu_old(self, effect_type):
    params= ('Speed','Quantity','Dynami','Primary Color','Secondary Color','Brightness','Palette', 'Direction', 'Primary Color','Secondary Color',)
        l_rainbow = [0,1,2,3]
        l_comet = ['Speed','Brightness','Color','Quantity']
        l_storm = ['Speed','Brightness','Color','Quantity']
        effects = [l_rainbow,l_comet,l_storm]
        return list(map(lambda x: params[x], l_rainbow),'''
'''
    def params_menu(self,params_list_no,params_type):
        #params_list_no - number of the list of parameters for the effect
        #params_type - type of the parameters, 0 - effect, 1 - settings, 9 - defined values

        params_dict = {0:('Params set',0,None), 1:('Brightness',0,7), 2: ('Speed',0,10), 3:('Quantity',1,50),4: ('Step',0,None), 5:('Color step',0,None),
                  6: ('Dynamic color',False,True),7: ('Length',0,None), 8:('Sections',0,None), 9: ('Direction',-1,1), 10:('Delay time',0,300,),
                  11:('Wait time',0,5000),12: ('Random factor',0.0,1.0),13:('Position offset',0,None), 14: ('Effect mode',0,3),
                  15: ('Multiplier mode',0,10),16: ('Color mode',0,6), 17:('Col mix method',0,2),18: ('Solid color',False, True),
                  30: ('Primary Color',0,None,self.color_menu()), 31: ('Secondary Color',0,None,self.color_menu()),32: ('Third color',0,None,self.color_menu()),
                  33: ('Palette-grd',0,None),34:('Palette-std',0,None),
                  50:('Buzzer',0,1), 51:('LCD Brightness',0,10)}

        # None means maximum value of the parameter, for colors 'DC' means defined colors, None means length of the palette
        # None for set means max number in set
        # False, True means False - off, True - on
        # -1,1 means -1 - counterclockwise, 1 - clockwise
        # TODO zrealizować dodatkowe menu do wyboru kolorów - zdefiniowanych, z palet lub ustawienie własnej wartości RGB

        l_rainbow = (2,5,6,9)
        settings = (50,51)
        # TODO: implement the rest of the parameters
        if params_type == 0:
            sub_list = (l_rainbow,)
        elif params_type == 1:
            sub_list = (settings,)
        elif params_type == 9:
            sub_list = (def_colors,)
        params = list(params_dict.get(x) for x in sub_list[params_list_no])
        return params,len(params)

    def params_sets(self,sub_list_no, params_set_no):
        l_rainbow = [[5,0,1,1],[50,5,1,-1]]
        params_sets = (l_rainbow,)
        return params_sets[sub_list_no][params_set_no], len(params_sets[sub_list_no][params_set_no])

    def color_menu(self,pal_type=0,palette_no=0):
        #TODO zaimplementować kolory z Aleds
        defined_colors = ('red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'purple', 'orange','pink', 'dark slate gray', 'dark green', 'dark blue','dark red', 'dark orange', 'dark magenta', 'dark cyan', 'dark violet','white', 'black')
        n_pal = normal_palettes[0]
        gr_pal = gradient_palettes[0]
        self.colors_list = (defined_colors,n_pal,gr_pal) # list of color palettes
        colors_menu = ['Std Palette','Grd Palette','Defined colors']
        return colors_menu[pal_type[palette_no]], len(colors_menu)


'''


'''
class MainScreen(CustomItem):
    def __init__(self, name):
        super().__init__(name)
        self._menu = None

    def bottom_menu(self,btm_no):
        btm_list = [['Effects','Elephants','TLines','Settings'],['','+1','+10','Back'],['Auto','Manual','','Back']]
        return btm_list[btm_no]

    def time_date(self, time, date):

        wr_dashb.set_textpos(0, 0)
        wr_dashb.printstring('12:34:56')
        wr_dashb.set_textpos(0, 100)
        wr_dashb.printstring(str(c.day) + '.' + str(c.month) + '.' + str(c.year))


class EffectList(CustomItem):

    def __init__(self, name):
        super().__init__(name)
        self._menu = None

    def prepare_list(self):
        import os
        files = os.listdir()
        self._menu = Menu(c.display, wr1, arial10, per_page = 4,x0 = 40, y0 = 20,m_width = 120)
        builder = MenuScreen('Files', self.parent)
        for file in files:
            builder.add(FilePreview(file))
        self._menu.set_screen(builder)

    def up(self):
        self._menu.move(-1)

    def down(self):
        self._menu.move()

    def select(self):
        self._menu.click()
        return self

    def draw(self):
        if self._menu is None:
            self.prepare_list()
        self._menu.draw()







class ParamsList(CustomItem):

    def __init__(self, name):
        super().__init__(name)
        self._menu = None

    def prepare_list(self):
        files = os.listdir()
        self._menu = Menu(c.display, wr_menu, arial10, per_page = 4,x0 = 40, y0 = 20,m_width = 120)
        builder = MenuScreen('Parameters', self.parent)
        for file in files:
            builder.add(FilePreview(file))
        self._menu.set_screen(builder)

    def up(self):
        self._menu.move(-1)

    def down(self):
        self._menu.move()

    def select(self):
        self._menu.click()
        return self

    def draw(self):
        if self._menu is None:
            self.prepare_list()
        self._menu.draw()



menu = Menu(c.display, wr1, arial10, per_page = 1,x0 = 0, y0 = 0,menu_header=False)
menu.set_screen(MenuScreen('').add(MainScreen('Show files')))
menu.draw()
'''
