from machine import Timer
from cl_umenu_wri import *     # updated Pawel Lugowski's umenu system to use Peter Hinch's nanogui library
from lib.switches import b_refresh
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

def check_buttons():
    
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
    b_refresh(False)

def etm():
    list_of_types = ['Light Effects', 'Gravity Effects', 'Sound Effects']#, 'Physical Effects']
    return list_of_types

def em(idx):
    light_eff = ['Solid'] #, 'Rainbow', 'Comet', 'Storm', 'Sparks', 'Madelaine', 'Mixer', 'Heartbeat']
    gravity_eff = ['Springs']#, 'Pong', 'Pendulum', 'Rolling stones', 'Rain', 'Snow', 'Particles', 'Sandglass']
    sound_eff = ['Spectrum']#, 'VU Meter', 'Sound Waves', 'Sound Particles', 'Sound Rush']
    #physical_eff = ['Clock']#, 'Sensors data', 'All together', 'Temperature', 'Humidity', 'Pressure']
    effects = (light_eff, gravity_eff, sound_eff)#, physical_eff)
    return effects[idx]

def pm(idx):
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
                   30: ('Primary Color', 0, None, color_menu()),
                   31: ('Secondary Color', 0, None, color_menu()), 32: ('Third color', 0, None, color_menu()),
                   33: ('Palette-grd', 0, None), 34: ('Palette-std', 0, None),
                   50: ('Buzzer', 0, 1), 51: ('LCD Brightness', 0, 10)}

    # None means maximum value of the parameter, for colors 'DC' means defined colors, None means length of the palette
    # None for set means max number in set
    # False, True means False - off, True - on
    # -1,1 means -1 - counterclockwise, 1 - clockwise
    # TODO zrealizować dodatkowe menu do wyboru kolorów - zdefiniowanych, z palet lub ustawienie własnej wartości RGB

    l_rainbow = (2, 5, 6, 9)
    sub_list = (l_rainbow,l_rainbow,l_rainbow,l_rainbow,l_rainbow,l_rainbow,l_rainbow,l_rainbow,l_rainbow,l_rainbow)
    # TODO: implement the rest of the parameters
    params = list(params_dict.get(x) for x in sub_list[idx])
    return params

def params_sets(self, sub_list_no, params_set_no):
    l_rainbow = [[5, 0, 1, 1], [50, 5, 1, -1]]
    params_sets = (l_rainbow,)
    return params_sets[sub_list_no][params_set_no], len(params_sets[sub_list_no][params_set_no])

def color_menu():
    pass

def led_menu(name, id):
    etm_menu = SubMenuItem(name)
    etm_menu.decorator = '|'+str(id)+'>'
    etm_menu.menu.title = str(id)
    for idx1, eff_type in enumerate(etm()):
        e_menu = (SubMenuItem(eff_type))
        e_menu.decorator = '|'+str(idx1)+'>'
        e_menu.menu.title = str(id)+str(idx1)
        for idx2, effect in enumerate(em(idx1)):
            #print('effect: ', idx2, effect)
            eff = SubMenuItem(effect)
            eff.decorator = '|'+str(idx2)+'>'
            eff.menu.title = str(id)+str(idx1)+str(idx2)
            for idx3, par in enumerate(pm(idx2)):    #pm(idx2)
                print(pm(idx2))
                param = ValueItem(par[0], 0, 0, 10, 1,print)
                #param = ValueItem('Speed', 10, 1, 100, 1, print)
                eff.add(param)
            e_menu.add(eff)
            #print('e_menu   first', e_menu.__dict__)
        #print('e_menu', e_menu.__dict__)
        etm_menu.add(e_menu)
    #print('etm_menu', etm_menu.__dict__)
    return etm_menu

# menu composition
c.progress(1)
menu = Menu(c.display, per_page= 6,line_height=12,x0=0,y0=0, m_width=92,menu_header=False)
screen = MenuScreen('MAIN MENU')
led1 = led_menu('LED1', 1)
led2 = led_menu('LED2', 2)
menu.set_screen(screen
            .add(led1)
            .add(led2)
            .add(SubMenuItem('Main Info'))
            .add(SubMenuItem('Settings')
                .add(SubMenuItem('Gamma Table')
                    .add(ValueItem('Gamma factor', c.gamma_table.gamma_factor(), 1, 4, 0.1, c.change_gamma_factor, 1))
                    .add(EnumItem("Gamma corr.", ['Off', 'On'], c.gamma_activation, int(c.gamma)))
                    .add(InfoItem("Table length:", decorator=c.get_gamma_length, visible=1)))
                .add(ValueItem('Color of menu', 15, 0, len(fss) - 1, 1, change_menu_color, 1))
                .add(EnumItem("Buzzer", ['On', 'Off'], c.buzzer_sound, 0)))
            .add(SubMenuItem('Status')
                .add(InfoItem('Status:', 'ok'))
                .add(InfoItem('Temp:', '45.1')))
            )
c.progress(1)
menu.draw()

async def switch_handler():
    while True:
        if c.display_refresh:  # display refresh is needed
            # print(c.hour,c.minutes,c.seconds,c.year,c.month,c.day,c.weekday)
            # print(c.temperature,c.humidity,c.pressure)
            c.display_refresh = False
            menu.draw()
            # try:
            #    if menu.current_screen.title[0:3] != 'LED':
            #        menu.draw()
            # except:
            #    menu.draw()

        if c.encoder.value() != 0:
            menu.move(c.encoder.value())
            c.encoder.value(0)
            c.beep(1)
        if c.encoder.state_value() != 0:
            menu.click()
            c.encoder.clear_button_state()
            c.beep()
        if b_refresh():
            check_buttons()


        asyncio.sleep_ms(50)


asyncio.run(switch_handler())

'''

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

    def effects_menu(self, effect_type):

        light_eff = ['Solid','Rainbow','Comet','Storm','Sparks','Madelaine','Mixer','Heartbeat']
        gravity_eff = ['Springs','Pong','Pendulum','Rolling stones','Rain','Snow','Particles','Sandglass']
        sound_eff = ['Spectrum','VU Meter','Sound Waves','Sound Particles','Sound Rush']
        physical_eff = ['Clock','Sensors data','All together','Temperature','Humidity','Pressure']
        effects = (light_eff,gravity_eff,sound_eff,physical_eff)
        self.effect_type = effect_type
        return effects[effect_type], len(effects[effect_type])
'''
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








class ParamsList(CustomItem):

    def __init__(self, name):
        super().__init__(name)
        self._menu = None

    def prepare_list(self):
        files = os.listdir()
        self._menu = Menu(c.display, wr_menu, arial10, per_page = 4,x0 = 40, y0 = 20,m_width = 120)
        screen_etm = MenuScreen('Parameters', self.parent)
        for file in files:
            screen_etm.add(FilePreview(file))
        self._menu.set_screen(screen_etm)

    def up(self):
        self._menu.move(-1)

    def down(self):
        self._menu.move()

    def select(self):
        self._menu.click()
        return self

    def draw(self):
        if self._menu is None:
          ! self.prepare_list()
        self._menu.draw()



menu = Menu(c.display, wr1, arial10, per_page = 1,x0 = 0, y0 = 0,menu_header=False)
menu.set_screen(MenuScreen('').add(MainScreen('Show files')))
menu.draw()
'''
