from machine import Pin, SoftI2C, I2S, SPI, RTC, Timer, freq
import gc
from lib.st7735r import ST7735R as TFT
from lib.switches import Button, RotaryEncoder
from cl_palettes import Palette, GammaTable
from lib.bme280 import BME280
from lib.ds3231 import DS3231
from cl_adr_leds import Aleds
from ulab import numpy as np  # !!! uncoment after finishing code)
# import numpy as np   # comment after writing the code - only for Pycharm
from cl_palettes import normal_palettes, gradient_palettes  # imports variables containing color palettes
from cl_palettes import red, green, blue, white, black, yellow, cyan, magenta, purple, orange, def_colors
# import uasyncio as asyncio
import time
from lib.writer import CWriter

### from el_effects import Effects


# display, bme, ds, rtc, buzzer, mv_raw_sound_samples,


class Segment():

    def __init__(self, id, segment, aled, active=False):
        self.id = id
        self.segment = segment
        self.aled_object = aled
        self.seg_length = len(self.segment)
        self.active = active

        self.seg_palette_active = False
        self.seg_palette_gamma_corrected = False
        self.colors_pst = [[0, 0, 0],[100, 100, 0],[200, 200, 0]]  # solid colors for the segment
        self.color_step = 1
        self.color_offset = 0


        self.direction = True  # True means clockwise, False counterclockwise
        # maybe instead of lists use numpy arrays???
        self.seg_palette = []  # ?????
        self.particles_list = []  # ????
        self.particle_length_list = []  # ????
        self.positions_list = []  # ????
        self.intensity_list = []  # ????

        self.segment_brightness = 5  # range (0..7), brightness bit shifting adjustments, shif left or right
        self.set_speed()

    def set_speed(self, speed=10):  # speed 0..10
        self.speed = speed
        self.period = 1000 // self.speed

    def lerp(self, a, b, t):
        return a + (b - a) * t

    def set_seg_palette(self, pal_length=None, palette_no=0, gradient=False):
        if pal_length == None: pal_length = self.seg_length
        self.seg_palette = Palette(pal_length=None, palette_no=0, gradient=False).palette
        self.seg_palette_active = True
        self.seg_palette_gamma_corrected = False

    def clear_seg_palette(self):
        self.seg_palette.clear()
        self.seg_palette_active = False
        self.seg_palette_gamma_corrected = False

    def set_segment_brightness(self, brightness):  # 0..7
        self.segment_brightness = brightness


class Led(Segment):
    # segments = i.e.[seg0, seg1, seg2, seg3, seg4]
    # first create segment instances and pass as a list to the device
    def __init__(self, id, segments, aled=None):
        self.id = id
        self.aled_object = aled
        self.segments = segments
        self.led_active = False
        self.device_brightness = 7
        if self.id == 1:
            self.current_segment = 0
        elif self.id == 2:
            self.current_segment = 4
        self.active_segments = []
        self.active_segments_string = ''
        self.only_active_segments = []
        self.check_active_segments()
        self.make_segments_string()
        self.make_only_active_segments_list()
        self.led_buffer = aled.aled_buffer
        self.led_buffer_adr = aled.aled_buffer_addr

        self.led_palette_active =False
        self.led_palette_gamma_corrected = False
        self.palette_type = 'N'  # N - normal, G - gradient, S - Solid color (no palette)
        self.led_palette = []
        self.palette_no = 0
        self.palette_length = None
        self.palette_gradient = False
        self.set_led_palette( pal_length=self.palette_length, palette_no=self.palette_no, gradient=self.palette_gradient)
        self.solid_color = [0,0,0]
        self.color_pst = 0


        self.general_speed = 5
        self.auto_mode = True
        self.auto_mode_time = 100
        # current effect number
        self.current_effect_no = 0

        self.auto_mode_effects = []
        self.auto_mode_params = []
        self.auto_mode_current_effect_no = 0

    def add_auto_mode_effects(self, effect, params):
        self.auto_mode_effects.append(effect)
        self.auto_mode_params.append(params)

    def check_active_segments(self):
        self.active_segments.clear()
        for _segment in self.segments:
            self.active_segments.append(_segment.active)  # list of active segments
        return self.active_segments

    def set_current_segment(self,seg=None):
        if seg == 'All inactive':
            self.current_segment = None
        else:
            self.current_segment = int(seg)
        return

    def set_active_segment(self, active_segment, flag=True):
        active_segments_list_length = len(self.active_segments)
        if flag == None:
            flag = not self.segments[active_segment].active
        if flag == True:
            if active_segment == 0:
                self.segments[0].active = True
                for i in range(1, active_segments_list_length):
                    self.segments[i].active = False
            elif active_segment > 0 and active_segment < (active_segments_list_length - 1):
                self.segments[active_segment].active = True
                self.segments[0].active = False
                self.segments[-1].active = False
            elif active_segment == active_segments_list_length - 1:
                self.segments[-1].active = True
                for i in range(0, active_segments_list_length - 1):
                    self.segments[i].active = False
            else:
                # set all segments as inactive if active_segment not in range
                for i in range(0, active_segments_list_length):
                    self.segments[i].active = False
        else:
            self.segments[active_segment].active = False
        self.check_active_segments()
        self.make_segments_string()
        self.make_only_active_segments_list()
        return self.get_active_segments(active_segment) # return active segment status

    def get_active_segments(self, segment=None):
        if segment != None:
            return self.active_segments[segment]
        else:
            return self.active_segments

    def make_segments_string(self):
        self.active_segments_string = ''
        for s in self.active_segments:
            self.active_segments_string += str(int(s))
        return self.active_segments_string  # return list of statuses as binary values in string format

    def make_only_active_segments_list(self):
        self.only_active_segments.clear()
        for i, s in enumerate(self.active_segments):
            if s == True:
                self.only_active_segments.append(str(i))
            else:
                continue
        if self.only_active_segments == []:
            self.only_active_segments.append('All inactive')
        return self.only_active_segments  # return list of statuses as binary values in string format but only active ones


    def set_led_palette(self, pal_length=None, palette_no=0, gradient=False):
        self.led_palette = Palette(pal_length=None, palette_no=0, gradient=False, order=[1, 0, 2, 3]).palette
        self.led_palette_active = True
        self.led_palette_gamma_corrected = False

    def clear_led_palette(self):
        self.led_palette.clear()
        self.led_palette_active = False
        self.led_palette_gamma_corrected = False


    '''def palette_mode(self, mode):
        if mode.startswith('L'):
            flag_l = True
            flag_s = False
        else:
            flag_l = False
            flag_s = True

        self.led_palette_active = flag_l
        try:
            for i,s in self.active_segments:
                if s: self.segments[i].seg_palette_active = flag_s
        except:
            return'''

    def led_palette_type(self, pal):
        if pal.startswith('N'):
            self.palette_type = 'N'
        elif pal.startswith('G'):
            self.palette_type = 'G'
        elif pal.startswith('S'):
            self.palette_type = 'S'
        else:
            return

    def set_color_pal_step(self, step=0):
        self.segments[self.current_segment].color_step = step
        return

    def set_color_pal_offset(self, offset=0):
        self.segments[self.current_segment].color_offset = offset
        return

    def set_pal_color(self, color_no):
        self.set_solid_color(self.led_palette[color_no])
        return

    def set_solid_r(self, value):
        self.set_solid_color(value, 'r')
        return

    def set_solid_g(self, value):
        self.set_solid_color(value, 'g')
        return

    def set_solid_b(self, value):
        self.set_solid_color(value, 'b')
        return

    def set_solid_color(self, c_value, color_component=None):
        if color_component == 'r':
            self.solid_color[0] = c_value
        elif color_component == 'g':
            self.solid_color[1] = c_value
        elif color_component == 'b':
            self.solid_color[2] = c_value
        elif isinstance(c_value, list):
            self.solid_color = c_value
        else:
            return

    def check_if_solid(self):
        if self.palette_type == 'S':
            return True
        else:
            return False

    def set_active_color_pst(self, pst):
        if pst.startswith('P'):
            self.color_pst = 0
        elif pst.startswith('S'):
            self.color_pst = 1
        elif pst.startswith('T'):
            self.color_pst = 2
        else:
            return

    def set_color(self):
        self.segments[self.current_segment].colors_pst[self.color_pst] = self.solid_color
        return

class Controller(Led):

    # leds - led object (lamp or device with some quantity of addressable leds)
    def __init__(self):
        # set the CPU frequency to 240 MHz
        freq(240000000)
        self.first_run = True
        self.ds_set = False
        self.rtc_set = False
        self.time_refreshed = False         # used to check if time was updated
        self.sensor_refreshed = False       # used to check if sensor data was updated
        self.display = None
        self.display_brightness = 7
        self.display_active = True
        self.set_display()
        self.progress(0)
        self.set_initial_date_and_time()
        self.gamma = True
        self.gamma_table = GammaTable()
        self.progress(1)
        self.init_hardware()
        self.clock_led = True  # display clock on addressable leds
        self.sensor_led = False  # display temperature, humidity and pressure on addressable leds
        self.buzzer_active = True
        self.controller_reset = False
        self.display_refresh = True
        self.progress(1)

    def progress(self, n):
        # Initialise and clear display.
        if n == 0:
            self.n = 0
        else:
            self.n += n
        # r, g, b = normal_palettes[1][self.n * 5]
        if self.n == 0:
            self.display.fill(0)
            self.display.text('Initialization', 24, 52, self.display.rgb(normal_palettes[1][self.n * 5]))
        else:
            self.display.text('#', 4 + 9 * self.n, 62, self.display.rgb(normal_palettes[1][self.n * 5]))
        self.display.show()

    # hardware initialization section
    def init_hardware(self):

        self.gc_mem_free()
        self.set_i2c()
        self.progress(1)
        self.set_ds()
        self.set_bme()
        self.set_rtc()
        self.progress(1)
        self.set_i2s()
        self.progress(1)
        self.set_buzzer()
        self.progress(1)
        self.set_buttons()
        self.progress(1)
        self.set_led1(1,72)
        self.progress(1)
        self.set_led2(3,144)
        self.set_timer()
        self.progress(1)
        self.gc_collect()
        self.display_refresh = True

    def set_display(self):

        # LCD TFT display configuration
        dc = Pin(2, Pin.OUT, value=1)  # Arbitrary pins
        cs = Pin(5, Pin.OUT, value=1)
        rst = Pin(4, Pin.OUT, value=1)
        # Hardware SPI on native pins for performance. Check DRIVERS.md for optimum baudrate.
        spi = SPI(2, 60_000_000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
        gc.collect()
        gc.mem_free()
        self.display = TFT(spi, cs, dc, rst)
        # On st7735r 1.8 inch display can exchange height and width for portrait mode. See docs.
        # Released under the MIT License (MIT). See LICENSE.
        # Copyright (c) 2020 Peter Hinch

    def set_timer(self, period=1000, active=True):
        # Timer configuration
        self.timer = Timer(0)
        if active:
            self.timer.init(period=period, mode=Timer.PERIODIC, callback=lambda t: self.get_data())
        else:
            self.timer.deinit()

    def set_i2s(self):
        # setup i2s bus and microphone
        SAMPLE_RATE = 32000
        SAMPLES_PER_FRAME = 256

        BITS = 16
        # Initialize I2S bus
        i2s = I2S(
            0,
            sck=Pin(13),
            ws=Pin(14),
            sd=Pin(34),
            mode=I2S.RX,
            bits=BITS,
            format=I2S.MONO,
            rate=SAMPLE_RATE,
            ibuf=4096
        )
        NUM_BYTES = BITS // 8
        raw_sound_samples = np.array([0] * SAMPLES_PER_FRAME, dtype=np.uint16)
        self.mv_raw_sound_samples = memoryview(raw_sound_samples)  # memoryview(raw_sound_samples) - samples buffer

    def set_i2c(self):
        # I2C interface initialization and pin assignment
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=1000000, timeout=50000)
        ###scan if adresses are not known
        # i2c_scan = i2c.scan()
        # for name in i2c_scan:
        #    print('I2C interface adress',hex(name), name)

    def set_bme(self):
        # global bme
        # BME280 sensor initialization
        try:
            self.bme = BME280(i2c=self.i2c)  # temperature, humidity and pressure sensor
            self.temperature = self.bme.temperature
            self.humidity = self.bme.humidity
            self.pressure = self.bme.pressure
        except:
            return 'BME280 ERROR'

    def set_ds(self):
        # DS3231 & RTC initialization

        try:
            self.ds = DS3231(self.i2c)  # real time clock
            # datetime get format = (year, month, monthday, weekday, hour, minute, second, 0)
            self.year, self.month, self.day, self.weekday, self.hour, self.minutes, self.seconds, _ = self.ds.datetime()
            self.ds_set = True
        except:
            self.set_initial_date_and_time()
            self.ds_set = False

            # self.ds.alarm_int(1, 2)  # enable alarm interrupt
            # self.ds.alarm2((2), match=self.ds.AL2_EVERY_M)  # set alarm1 to trigger every minute

    def set_rtc(self):
        self.rtc = RTC()
        try:
            self.rtc.datetime(self.ds.datetime())  # set the DS3231 time to the RTC time
            # datetime get format = (year, month, monthday, weekday, hour, minute, second, 0)
            self.rtc_set = True
        except:
            self.set_initial_date_and_time()
            self.rtc.datetime((self.year, self.month, self.day,self.day_of_week(self.year,self.month,self.day) , 0, 0, 0, 0))
            self.rtc_set_flag = True


    def set_buttons(self):
        # Button configuration
        self.b_left = Button(32, powering='GND')
        self.b_right = Button(26, powering='GND')
        self.b_minus = Button(33, powering='GND')
        self.b_plus = Button(25, powering='GND')
        self.b_light = Button(17, powering='GND')
        self.b_set_rtc = Button(16, powering='GND')
        self.encoder = RotaryEncoder(34, 35, 36, powering='GND', direction='CW')

    def set_buzzer(self):
        # Buzzer configuration
        self.buzzer = Pin(15, Pin.OUT)
        # self.pwm = PWM(self.buzzer, freq=30, duty_u16=8192)

    # setup of addressable leds:
    ## led buffers
    def set_led1(self,x,y):
        # led1 buffer
        n = x*y
        el_leds_buffer = np.array(n * [[0, 0, 0]], dtype=np.uint8)
        # memoryview of the buffers
        el_mv = memoryview(el_leds_buffer)
        # LED strip object initialization
        el_leds = Aleds(27, el_mv, n, bpp=3, order=[1, 0, 2, 3])  # init of elephant lamp NeoPix object
        # Segments of the elephant lamp
        self.progress(1)
        seg0 = Segment(0, el_leds_buffer[:], el_leds, True)  # all
        seg1 = Segment(1, el_leds_buffer[:36], el_leds)  # circle
        seg2 = Segment(2, el_leds_buffer[36:48], el_leds)  # elephants
        seg3 = Segment(3, el_leds_buffer[48:], el_leds)  # trees
        seg4 = Segment(4, [seg1, seg2, seg3], el_leds)  # matrix for future # put matrix from elephants ?!?!?!? #
        # set led lamp object
        self.led1 = Led(1, [seg0, seg1, seg2, seg3, seg4], el_leds, )
        # gamma correction of the palette
        ## print(self.led1.led_palette) # before gamma - debug purposes only
        if self.gamma == True:
            self.led1.led_palette = self.gamma_table.gamma_cor(self.led1.led_palette)
            self.led1.led_palette_gamma_corrected = True
        self.progress(1)
        ## print(self.led1.led_palette) # after gamma - debug purposes only
        # aled_fill black (turn off) all leds
        self.led1.aled_object.aled_fast_fill(self.led1.led_buffer, (n * 3) // 4, 0)
        self.led1.aled_object.write()

    def set_led2(self,x,y):
        # led2 buffer
        n = x*y
        tl_leds_buffer = np.array(n * [[0, 0, 0]], dtype=np.uint8)
        # memoryview of the buffers
        tl_mv = memoryview(tl_leds_buffer)
        # LED strip object initialization
        tl_leds = Aleds(3, tl_mv, n, bpp=3, order=[1, 0, 2, 3])  # init of three led lines NeoPix object
        self.progress(1)
        # Segments of the three led lines
        seg5 = Segment(5, tl_leds_buffer[:], tl_leds)  # all leds
        seg6 = Segment(6, tl_leds_buffer[:y], tl_leds)  # first line
        seg7 = Segment(7, tl_leds_buffer[y:(2*y)], tl_leds)  # second line, remember to flip (np.flip(seg6,axis=0) segment and pass to the tl_leds_buffer before sending to the led strip
        seg8 = Segment(8, tl_leds_buffer[(2*y):], tl_leds)  # third line
        seg9 = Segment(9, [seg6, seg7, seg8], tl_leds, True)  # matrix
        # set led2 lamp object
        self.led2 = Led(2, [seg5, seg6, seg7, seg8, seg9], tl_leds)

        # gamma correction of the palette
        if self.gamma == True:
            self.led2.led_palette = self.gamma_table.gamma_cor(self.led2.led_palette)
        self.progress(1)
        # aled_fill black (turn off) all leds
        self.led2.aled_object.aled_fast_fill(self.led2.led_buffer, (n * 3) // 4, 0)
        self.led2.aled_object.write()

    def get_led_device(self, id):
        leds = (None, self.led1, self.led2)
        return leds[id]

    def gc_collect(self):
        gc.collect()  # collect garbage

    def gc_mem_free(self):
        gc.mem_free()  # free memory

    def buzzer_sound(self, state='On'):
        if state == 'On':
            self.buzzer_active = True
        elif state == 'Off':
            self.buzzer_active = False
        return

    def beep(self, duration=10):
        if self.buzzer_active:
            self.buzzer.on()
            time.sleep_ms(duration)
            self.buzzer.off()
        else:
            return  # exit from the function

    # sensor section:
    def get_sensor_data(self):
        t = self.temperature
        h = self.humidity
        p = self.pressure

        try:
            t = self.bme.temperature
        except:
            self.temperature = '---'

        try:
            h = self.bme.humidity
        except:
            self.humidity = '---'

        try:
            p = self.bme.pressure
        except:
            self.pressure = '---'

        if self.temperature != t or self.humidity != h or self.pressure != p:
            self.temperature = t
            self.humidity = h
            self.pressure = p
            self.sensor_refreshed = True
        else:
            self.sensor_refreshed = False

    # date and time section:
    def leap_year(self, year):
        return bool((not year % 4) ^ (not year % 100))

    def get_month_length(self, month, d=bytearray((31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31))):
        days = d[month - 1]
        return days if days else (29 if self.leap_year(self.year) else 28)

    def day_of_week(self, year, month, day):
        t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
        year -= month < 3
        return ((year + year // 4 - year // 100 + year // 400 + t[month - 1] + day)-1) % 7
        # -1 to scale it to 0..6 as in rtc library, changed also in ds3231 driver

    def get_name_of_the_day(self, wday, days=('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')):
        return days[wday]

    def get_time(self):
        h_str = self.prefix(self.hour)
        m_str = self.prefix(self.minutes)
        s_str = self.prefix(self.seconds)
        return h_str, m_str, s_str

    def get_date(self):
        y_str = str(self.year)
        m_str = self.prefix(self.month)
        d_str = self.prefix(self.day)
        w_str = self.get_name_of_the_day(self.weekday)
        return d_str, m_str, y_str, w_str

    def set_rtc_time(self, year, month, day, hour, minutes, seconds):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minutes = minutes
        self.seconds = seconds
        self.weekday = self.day_of_week(year, month, day)
        time = (self.year, self.month, self.day, self.weekday, self.hour, self.minutes, self.seconds)
        try:
            # format for setting datetime for ds = (year, month, monthday, weekday, hour, minute, second) - changed in driver
            self.ds.datetime(time)
            self.rtc.datetime(self.ds.datetime())
            self.rtc_set_flag = True
        except:
            self.rtc_set_flag = False


    def set_initial_date_and_time(self):
        self.year = 2024
        self.month = 5
        self.day = 11
        self.weekday = self.day_of_week(self.year, self.month, self.day)
        self.hour = 0
        self.minutes = 0
        self.seconds = 0
    def update_time(self):
        datetime_now = self.rtc.datetime()
        # self.hour = self.datetime_now[4]
        # self.second = self.datetime_now[6]
        # self.day = self.datetime_now[2]
        # self.month = self.datetime_now[1]
        # self.year = self.datetime_now[0]

        if self.seconds != datetime_now[6]:
            self.year, self.month, self.day, self.weekday, self.hour, self.minutes, self.seconds, _ = datetime_now
            self.time_refreshed = True
        else:
            self.time_refreshed = False
    def prefix(self, number):
        if number < 10:
            return '0' + str(number)
        else:
            return str(number)

    def check_flags(self):
        if self.time_refreshed or self.sensor_refreshed:
            self.display_refresh = True

    def get_data(self):
        self.update_time()
        self.get_sensor_data()
        self.check_flags()

    #gamma table and set palettes section
    def gamma_activation(self, arg: str):
        if arg == 'On':
            self.gamma = True
            self.reset_gamma_table()
        elif arg == 'Off':
            self.gamma = False
            self.gamma_table.clear_gamma_table()
            self.reset_palettes()

    def change_gamma_factor(self, arg: float):
        if self.gamma_table.gamma_factor() != arg:
            self.gamma_table.gamma_factor(arg)
            self.reset_gamma_table()
        else:
            return

    def change_color_space(self, arg: int):
        if self.gamma_table.color_space() != arg:
            self.gamma_table.color_space(arg)
            self.reset_gamma_table()
        else:
            return
    def get_gamma_length(self):
        return str(len(self.gamma_table.gamma_table))
    def reset_gamma_table(self):
        if self.gamma == True:
            self.gamma_table.clear_gamma_table()
            self.gamma_table.create_gamma_table(self.gamma_table.gamma_factor(), self.gamma_table.color_space())
            if self.led1.led_palette_active == True or self.led1.led_palette_active == True:
                self.reset_palettes()
        else:
            return

    def reset_palettes(self):

        if self.led1.led_palette_active == True:
            self.led1.set_led_palette( pal_length=self.led1.palette_length, palette_no=self.led1.palette_no, gradient=self.led1.palette_gradient)
            if self.gamma == True:
                if self.led1.led_palette_gamma_corrected == False:
                    self.led1.led_palette = self.gamma_table.gamma_cor(self.led1.led_palette)
                    self.led1.led_palette_gamma_corrected = True
            else:
                self.led1.led_palette_gamma_corrected = False
        else:
            return

        if self.led2.led_palette_active == True:
            self.led2.set_led_palette(pal_length=self.led2.palette_length, palette_no=self.led2.palette_no, gradient=self.led2.palette_gradient)
            if self.gamma == True:
                if self.led2.led_palette_gamma_corrected == False:
                    self.led2.led_palette = self.gamma_table.gamma_cor(self.led2.led_palette)
                    self.led2.led_palette_gamma_corrected = True
            else:
                self.led2.led_palette_gamma_corrected = False
        else:
            return

    # segments methods

