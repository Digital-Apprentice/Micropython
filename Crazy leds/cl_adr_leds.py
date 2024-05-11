import uctypes
from machine import bitstream, Pin
import micropython
from cl_palettes import Palette
# normal_palettes, gradient_palettes
#import numpy as np  # comment in microcontroller - after finish
from ulab import numpy as np # uncoment on microcontroller
import gc

#in order to increase the processing speed, the timing is set rigidly for 800kHz diodes, the ORDER is for the GRB set and bpp = 3
#pass a memory view object or ndarray slice from numpy as a buffer using the set_buf method , data in bytearray format
#or pass uctypes.addressof(obj), check the method execution time

black = (0,0,0)

class Aleds():

    def __init__(self, pin, buffer, n, bpp=3, order=[1,0,2,3]):  # ORDER [G,R,B,W]
        self.pin = Pin(pin, Pin.OUT)
        self.set_buffer(buffer) # set buffer and their address, buffer is a memory view object or ndarray slice from numpy, or ndarray or array (bytearray format object)
        self.n = n
        self.bpp = bpp
        self.aled_buffer_len = len(buffer)
        self.aled_buffer_ff_len = self.aled_buffer_len // 4
        self.timing = (400, 850, 800, 450) #option omitted (((400, 850, 800, 450) if timing else (800, 1700, 1600, 900))
            #if isinstance(timing, int) else timing)


    def set_buffer(self, buffer):
        self.aled_buffer = buffer  # buffer is a memory view object or ndarray slice from numpy, or ndarray or array (bytearray format object
        self.aled_buffer_addr = uctypes.addressof(buffer)  # uctypes.addressof(buffer) returns the address of the buffer
    def __setitem__(self, i, c):  # v = trzy bajty koloru w odpowiednim porządku, bez sprawdzania i przestawiania danych
        self.aled_buffer[self.aled_buffer_addr + (i * self.bpp)] = c

    def __getitem__(self, i):
        return uctypes.bytearray_at(self.aled_buffer_addr+(i * self.bpp), self.bpp)

    #def __len__(self):  # do przepisania = długość macierzy
    #    return self.n

    @micropython.viper
    # fast filling with desired 32bit word as value
    # desired 32bit word, -1 give 0xffffffff, 0 give 0x00000000
    def aled_fast_fill(self, ba: ptr32, ba_len: int , value: int):
        for i in range(ba_len):
            ba[i] = value

        # przykład użycia:
        # ba4 = bytearray(315*4)
        # fill_viper4(ba4, len(ba4) // 4)
        # długość bufora przeliczyć dla liczby podzielnej przez 4, np. dla długości 420 po 3 bajty = 420 x 3 = 315 x 4
        # bufor wypełniany jest liczbami 32-bitowymi
        # w wywołaniu metody podajemy wskaźnik na tablicę bajtów oraz jej długość podzieloną bez reszty przez 4, bo liczby 32bitowe


    def aled_fill(self, c):  # v = one desired color (in three bytes format)
        b = self.aled_buffer
        l = len(self.aled_buffer)
        j = 0
        while j < l:
            self.aled_buffer[j] = c
            j += self.bpp

    def write(self, addr=None):  # addr = uctypes.addressof(obj)
        # BITSTREAM_TYPE_HIGH_LOW = 0
        bitstream(self.pin, 0, self.timing, uctypes.bytearray_at(self.aled_buffer_addr, self.n * self.bpp))

    #do przepisania i dostosowania do kolory w formacie bajtowym w odpowiednim porządku (order)
    # rozważyć przesunięcie bitowe poszczególnych składowych koloru r << 1..7
    def change_brightness(self, color, brightness):# brightness range [0..7] for RGB color space
        r,g,b = color
        if brightness <= 0:
            return (0,0,0)
        elif brightness <= 7:
            brightness = 7 - brightness
            return (r>>brightness,g>>brightness,b>>brightness)
        else:
            return (r,g,b)

    def set_all(self,color,brightness=127):
        if brightness == 127:
            self.aled_fill(color)
        else:
            self.aled_fill(self.change_brightness(color, brightness))

    def round_cooridinates(self, coordinates):
        # rounds coordinates for matrix indices
        points_rounded = []
        for point in coordinates:
            points_rounded.append((round(point[0]), round(point[1])))
        return points_rounded


