from machine import Timer
from cl_umenu_wri import *     # updated Pawel Lugowski's umenu system to use Peter Hinch's nanogui library
import uasyncio as asyncio
from cl_palettes import full_saturation_spectrum as fss

def change_menu_color(arg):
    menu.set_colors(c.display.rgb(fss[arg]), c.display.rgb(black))


def effects_menu(effect_type):

    list_of_types = ['Light Effects','Gravity Effects','Sound Effects','Physical Effects']

    light_eff = ['Solid','Rainbow','Comet','Storm','Sparks','Madelaine','Mixer','Heartbeat']
    gravity_eff = ['Springs','Pong','Pendulum','Rolling stones','Rain','Snow','Particles','Sandglass']
    sound_eff = ['Spectrum','VU Meter','Sound Waves','Sound Particles','Sound Rush']
    physical_eff = ['Clock','Sensors data','All together','Temperature','Humidity','Pressure']
    effects = (light_eff,gravity_eff,sound_eff,physical_eff)
    effect_type = effect_type
    return effects[effect_type], len(effects[effect_type])


def etm(name,screen):
    etm_menu = SubMenuItem(name)
    list_of_types = ['Light Effects', 'Gravity Effects', 'Sound Effects', 'Physical Effects']
    for idx, eff_type in enumerate(list_of_types):
        etm_menu.add(SubMenuItem(eff_type))
    return etm_menu


class Lists(CustomItem):

    def __init__(self, name, led, title, decorator, list_type):
        super().__init__(name)
        self._menu = None
        self.decorator = decorator
        self.led = led
        self.title = name + '-' + title
        self.list_type = list_type

    def prepare_menu(self):
        # prepare the menu for the first list of LED menu (type of effects)
        # the menu takes up the entire screen
        # refreshing every second is suspended and is only performed when there is a change in the menu-+

        self._menu = Menu(c.display, per_page=5, x0=0, y0=0, m_width=158, menu_header=True, draw_default=False)

    def prepare_screen(self):
        self._screen = MenuScreen(self.title, self.parent)

    def prepare_list(self):

        if self.list_type == 0:
            self.prepare_screen()
            self.prepare_menu()
            list_of_types =self.effects_menu(self.list_type)
        for idx, eff_type in enumerate(list_of_types):
            self._screen.add(CustomItem(eff_type),self.parent)

            self._menu.set_screen(self._screen)
        elif self.list_type == 1:
            pass
    def up(self):
        self._menu.move(-1)

    def down(self):
        self._menu.move()

    def select(self):
        item = self._screen.get(self._screen.selected)
        print('item',type(item))
        if type(item) is BackItem:
            return self.parent
        else:
            return self

    def draw(self):
        if self._menu is None:
            self.prepare_list()
        self._menu.draw()


def effects_menu(self, effect_type):
    light_eff = ['Solid', 'Rainbow', 'Comet', 'Storm', 'Sparks', 'Madelaine', 'Mixer', 'Heartbeat']
    gravity_eff = ['Springs', 'Pong', 'Pendulum', 'Rolling stones', 'Rain', 'Snow', 'Particles', 'Sandglass']
    sound_eff = ['Spectrum', 'VU Meter', 'Sound Waves', 'Sound Particles', 'Sound Rush']
    physical_eff = ['Clock', 'Sensors data', 'All together', 'Temperature', 'Humidity', 'Pressure']
    effects = (light_eff, gravity_eff, sound_eff, physical_eff)
    self.effect_type = effect_type
    return effects[effect_type], len(effects[effect_type])
def params_menu(self, params_list_no, params_type):
    # params_list_no - number of the list of parameters for the effect
    # params_type - type of the parameters, 0 - effect, 1 - settings, 9 - defined values

    params_dict = {0: ('Params set', 0, None), 1: ('Brightness', 0, 7), 2: ('Speed', 0, 10), 3: ('Quantity', 1, 50),
                   4: ('Step', 0, None), 5: ('Color step', 0, None),
                   6: ('Dynamic color', False, True), 7: ('Length', 0, None), 8: ('Sections', 0, None),
                   9: ('Direction', -1, 1), 10: ('Delay time', 0, 300,),
                   11: ('Wait time', 0, 5000), 12: ('Random factor', 0.0, 1.0), 13: ('Position offset', 0, None),
                   14: ('Effect mode', 0, 3),
                   15: ('Multiplier mode', 0, 10), 16: ('Color mode', 0, 6), 17: ('Col mix method', 0, 2),
                   18: ('Solid color', False, True),
                   30: ('Primary Color', 0, None, self.color_menu()),
                   31: ('Secondary Color', 0, None, self.color_menu()), 32: ('Third color', 0, None, self.color_menu()),
                   33: ('Palette-grd', 0, None), 34: ('Palette-std', 0, None),
                   50: ('Buzzer', 0, 1), 51: ('LCD Brightness', 0, 10)}

    # None means maximum value of the parameter, for colors 'DC' means defined colors, None means length of the palette
    # None for set means max number in set
    # False, True means False - off, True - on
    # -1,1 means -1 - counterclockwise, 1 - clockwise
    # TODO zrealizować dodatkowe menu do wyboru kolorów - zdefiniowanych, z palet lub ustawienie własnej wartości RGB

    l_rainbow = (2, 5, 6, 9)
    settings = (50, 51)
    # TODO: implement the rest of the parameters
    if params_type == 0:
        sub_list = (l_rainbow,)
    elif params_type == 1:
        sub_list = (settings,)
    elif params_type == 9:
        sub_list = (def_colors,)
    params = list(params_dict.get(x) for x in sub_list[params_list_no])
    return params, len(params)

def color_menu(self, pal_type=0, palette_no=0):
    # TODO zaimplementować kolory z Aleds
    defined_colors = (
    'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'purple', 'orange', 'pink', 'dark slate gray', 'dark green',
    'dark blue', 'dark red', 'dark orange', 'dark magenta', 'dark cyan', 'dark violet', 'white', 'black')
    n_pal = normal_palettes[0]
    gr_pal = gradient_palettes[0]
    self.colors_list = (defined_colors, n_pal, gr_pal)  # list of color palettes
    colors_menu = ['Std Palette', 'Grd Palette', 'Defined colors']
    return colors_menu[pal_type[palette_no]], len(colors_menu)

"""
class EffectList(CustomItem):

    def __init__(self, name, e, led, builder):
        super().__init__(name)
        self.effects_menu = None
        self.e = e
        self.led = led
        self.builder = builder

    def prepare_list(self):
        light_eff = ['Solid', 'Rainbow', 'Comet', 'Storm', 'Sparks', 'Madelaine', 'Mixer', 'Heartbeat']
        gravity_eff = ['Springs', 'Pong', 'Pendulum', 'Rolling stones', 'Rain', 'Snow', 'Particles', 'Sandglass']
        sound_eff = ['Spectrum', 'VU Meter', 'Sound Waves', 'Sound Particles', 'Sound Rush']
        physical_eff = ['Clock', 'Sensors data', 'All together', 'Temperature', 'Humidity', 'Pressure']
        effects = (light_eff, gravity_eff, sound_eff, physical_eff)
        #self.effects_menu = Menu(c.display, wr_menu, per_page=5, x0=0, y0=0, m_width=158, menu_header=True, draw_default=False)
        #screen_etm = MenuScreen('Type of Effects', self.parent)

        for idx, eff in enumerate(effects[self.e]):
            self.builder.add(SubMenuItem(eff))
        #self.effects_menu.set_screen(screen_etm)

    def up(self):
        self.builder.move(-1)

    def down(self):
        self.builder.move()

    def select(self):
        self.builder.click()
        return self

    def draw(self):
        if self.builder is None:
            self.prepare_list()
        self.builder.draw()
"""
menu = Menu(c.display, per_page= 6,line_height=12,x0=0,y0=0, m_width=92,menu_header=False)
screen = MenuScreen('MAIN MENU')
menu.set_screen(screen
            .add(SubMenuItem('Settings')
                .add(SubMenuItem('Gamma Table')
                    .add(ValueItem('Gamma factor', c.gamma_table.gamma_factor(), 1, 4, 0.1, c.change_gamma_factor, 1))
                    .add(EnumItem("Gamma corr.", ['Off', 'On'], c.gamma_activation, int(c.gamma)))
                    .add(InfoItem("Table length:", decorator=c.get_gamma_length, visible=1)))
                .add(ValueItem('Color of menu', 15, 0, len(fss) - 1, 1, change_menu_color, 1))
                .add(EnumItem("Buzzer", ['On', 'Off'], c.buzzer_sound, 0)))
            .add(etm('LED1', screen))
            .add(Lists('LED2',2,'Effect types, '_/\_', 0))
            .add(SubMenuItem('Main Info')
                .add(InfoItem('Status:', 'ok'))
                .add(InfoItem('Temp:', '45.1')))
            )
menu.draw()


async def switch_handler():
    while True:
        if c.display_refresh:  # display refresh is needed
            #print(c.hour,c.minutes,c.seconds,c.year,c.month,c.day,c.weekday)
            #print(c.temperature,c.humidity,c.pressure)
            c.display_refresh = False
            if menu.current_screen.title == 'MAIN MENU':
                menu.draw()
        if c.encoder.value() != 0:
            menu.move(c.encoder.value())
            c.encoder.value(0)
            c.beep(1)
        if c.encoder.state_value() != 0:
            menu.click()
            c.encoder.clear_button_state()
            c.beep()
        if c.b_left.state_value() != 0:
            if c.b_left.state_value() == 1:
                c.led1.led_active = not c.led1.led_active
            elif c.b_left.state_value() == -1:
                c.led1.auto_mode = not c.led1.auto_mode
            c.b_left.clear_button_state()
            c.display_refresh = True
        if c.b_right.state_value() != 0:
            if c.b_right.state_value() == 1:
                c.led2.led_active = not c.led2.led_active
            elif c.b_right.state_value() == -1:
                c.led2.auto_mode = not c.led2.auto_mode
            c.b_right.clear_button_state()
            c.display_refresh = True
        if c.b_minus.state_value() != 0:
            c.sensor_led = not c.sensor_led
            c.b_minus.clear_button_state()
            c.display_refresh = True
        if c.b_plus.state_value() != 0:
            c.clock_led = not c.clock_led
            c.b_plus.clear_button_state()
            c.display_refresh = True
        asyncio.sleep_ms(80)


asyncio.run(switch_handler())

'''

#########################################

class Menu(object):
    
    def __init__(self, name, top=None, btm=None, sub=None, eff=None, param=None):
        
        self.effect_type = eff                # number of the effect
        self.param_no = param               # parameter level - deepness of the parameter, 0 is the default parameter
        self.effect_selected= 0             # selected effect
        self.params_list_selected = 0       # selected list of parameters
        self.params_set = 0                 # selected set of parameters


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
