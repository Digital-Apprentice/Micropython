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
from gui.core.writer import CWriter

### from el_effects import Effects

def_colors.extend(['R', 'RM'])


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
    def __init__(self, id, segments=None, aled=None):
        self.id = id
        self.aled_object = aled
        self.segments = segments
        self.active_segments = []
        self.set_active_segment()
        self.led_buffer = aled.aled_buffer
        self.led_buffer_adr = aled.aled_buffer_addr

        self.led_palette_active = False
        self.led_palette_gamma_corrected = False
        self.led_palette = []
        self.set_led_palette()
        self.led_active = False
        self.device_brightness = 7
        self.general_speed = 5
        self.auto_mode = True
        self.auto_mode_time = 100
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

    def set_active_segment(self, active_segment=0, flag=False):
        self.check_active_segments()
        active_segments_list_length = len(self.active_segments)
        if flag == True:
            if active_segment == 0:
                self.active_segments[0] = True
                for i in range(1, active_segments_list_length):
                    self.active_segments[i] = False
            elif 0 < active_segment < active_segments_list_length - 1:
                self.active_segments[active_segment] = True
                self.active_segments[0] = False
                self.active_segments[-1] = False
            elif active_segment == active_segments_list_length - 1:
                self.active_segments[-1] = True
                for i in range(0, active_segments_list_length - 1):
                    self.active_segments[i] = False
            else:
                # set all segments as inactive if active_segment not in range
                for i in range(0, active_segments_list_length):
                    self.active_segments[i] = False
        else:
            self.active_segments[active_segment] = False

    def set_led_palette(self, pal_length=None, palette_no=0, gradient=False):
        self.led_palette = Palette(pal_length=None, palette_no=0, gradient=False, order=[1, 0, 2, 3]).palette
        self.led_palette_active = True
        self.led_palette_gamma_corrected = False

    def clear_led_palette(self):
        self.led_palette.clear()
        self.led_palette_active = False
        self.led_palette_gamma_corrected = False


class Controller(Led):

    # leds - led object (lamp or device with some quantity of addressable leds)
    def __init__(self):
        # set the CPU frequency to 240 MHz
        freq(240000000)
        self.first_run = True
        self.ds_set = False
        self.rtc_set = False
        self.time_refreshed = False
        self.sensor_refreshed = False
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
        self.humidity_led = False  # display humidity on addressable leds
        self.temperature_led = False  # display temperature on addressable leds
        self.pressure_led = False  # display pressure on addressable leds
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

        self.progress(1)
        self.gc_mem_free()
        self.set_i2c()
        self.progress(1)
        self.set_ds()
        self.progress(1)
        self.set_bme()
        self.progress(1)
        self.set_i2s()
        self.progress(1)
        self.set_rtc()
        self.set_buzzer()
        self.progress(1)
        self.set_buttons()
        self.progress(1)
        self.set_led1(72)
        self.progress(1)
        self.set_led2(144*3)
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
        self.ds = DS3231(self.i2c)    # real time clock
        try:
            self.ds = DS3231(self.i2c)  # real time clock
            # datetime get format = (year, month, monthday, weekday, hour, minute, second, 0)
            self.year, self.month, self.day, self.weekday, self.hour, self.minutes, self.seconds,_ = self.ds.datetime()
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
            self.rtc.datetime((self.year, self.month, self.day,self.day_of_week(self.day,self.month,self.year) , 0, 0, 0, 0))
            self.rtc_set_flag = True


    def set_buttons(self):
        # Button configuration
        self.b_left = Button(32, powering='GND')
        self.b_right = Button(26, powering='GND')
        self.b_minus = Button(33, powering='GND')
        self.b_plus = Button(25, powering='GND')
        self.b_light = Button(39, powering='POS')
        self.b_set_rtc = Button(36, powering='POS')
        self.encoder = RotaryEncoder(17, 16, 12, powering='GND', direction='CW')

    def set_buzzer(self):
        # Buzzer configuration
        self.buzzer = Pin(15, Pin.OUT)
        # self.pwm = PWM(self.buzzer, freq=30, duty_u16=8192)

    # setup of addressable leds:
    ## led buffers
    def set_led1(self,n):
        # led1 buffer
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

    def set_led2(self,n):
        # led2 buffer
        tl_leds_buffer = np.array(n * [[0, 0, 0]], dtype=np.uint8)
        # memoryview of the buffers
        tl_mv = memoryview(tl_leds_buffer)
        # LED strip object initialization
        tl_leds = Aleds(0, tl_mv, n, bpp=3, order=[1, 0, 2, 3])  # init of three led lines NeoPix object
        self.progress(1)
        # Segments of the three led lines
        seg5 = Segment(5, tl_leds_buffer[:], tl_leds)  # all leds
        seg6 = Segment(6, tl_leds_buffer[:140], tl_leds)  # first line
        seg7 = Segment(7, tl_leds_buffer[140:280], tl_leds)  # second line, remember to flip (np.flip(seg6,axis=0) segment and pass to the tl_leds_buffer before sending to the led strip
        seg8 = Segment(8, tl_leds_buffer[280:], tl_leds)  # third line
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

    def gc_collect(self):
        gc.collect()  # collect garbage

    def gc_mem_free(self):
        gc.mem_free()  # free memory
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

    def day_of_week(self, day, month, year):
        t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
        year -= month < 3
        return (year + year // 4 - year // 100 + year // 400 + t[month - 1] + day) % 7

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
        self.weekday = self.day_of_week(day, month, year)
        time = (self.year, self.month, self.day, self.hour, self.minutes, self.seconds, self.weekday)
        try:
            # format for setting datetime for ds = (year, month, monthday, hour, minute, second, weekday)
            self.ds.datetime(time)
            self.rtc.datetime(self.ds.datetime())
            self.rtc_set_flag = True
        except:
            self.rtc_set_flag = False


    def set_initial_date_and_time(self):
        self.year = 2024
        self.month = 5
        self.day = 11
        self.weekday = self.day_of_week(self.day, self.month, self.year)
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
        if self.time_refreshed or self.sensor_refreshed or self.controller_reset:
            self.display_refresh = True

    def get_data(self):
        self.update_time()
        self.get_sensor_data()
        self.check_flags()


