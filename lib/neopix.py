# copyright Tomasz Zgrys (Digital-Apprentice) - 2022 - MIT license 
# only for RGB leds (not RGBW)


from machine import Pin
from neopixel import NeoPixel
import time

# lightning_form:
#                'strip' = leds_in_col = number of leds, num_of_cols = 1 , if strip, this parameter does not need to be specified
#                'matrix': leds_in_col = leds quantity in column or in a strip if only one column, num_of_cols = leds quantity in row if matrix or 1 if strip
#                          for matrix in which leds are placed in chain, indexes in every even column start from bottom, in odd column from top
#                          like this: matrix[[0,1,2,3],[7,6,5,4],[8,9,10,11],[15,14,13,12],...]

# References:
# http://en.wikipedia.org/wiki/HSV_color_space



class NeoPix:
    def __init__(self, data_pin, lightning_form, leds_in_col, num_of_cols=1, bpp=3, timing=1, cor_gamma=True, gamma=2.2, brightness_space = 8 ):       
        # data_pin is a machine.Pin instance.
        # bpp is 3 for RGB LEDs, and 4 for RGBW LEDs.
        # timing is 0 for 400KHz, and 1 for 800kHz LEDs (most are 800kHz)
        self._leds_in_col = leds_in_col
        self._num_of_col = num_of_cols
        self.bpp = bpp
        aled_data_pin = Pin(data_pin,Pin.OUT)
        if lightning_form == 'strip':
            self.aled = NeoPixel(aled_data_pin, leds_in_col, bpp, timing)
        elif lightning_form == ('chain_matrix' or 'standard_matrix'): 
            self.led_matrix(lightning_form, num_of_cols, leds_in_col)
            self.aled = NeoPixel(aled_data_pin,self.leds_count, bpp, timing)      
        if cor_gamma: self.gamma_table(gamma)      
    
    def gamma_table(self, gamma_factor, brightness_space = 8):  # 8-bit brightness space, only one table for all colors
        self.gamma_factor = gamma_factor
        brightness_space = pow(2,brightness_space)-1
        #print('brightness_space',brightness_space) # for debugging purposes only
        self._gamma_table = []
        i = 0
        for i in range (brightness_space+1):
            self._gamma_table.append(round(brightness_space*(i/brightness_space)**self.gamma_factor+0.4))
        #print('len gamma, table',len(self._gamma_table),self._gamma_table)    # for debugging purposes only
        
    def leds_in_col(self):
        return self._leds_in_col
    
    def num_of_col(self):
        return self._num_of_col
    
    def get_gamma(self,position):
        return self._gamma_table[position]
    
    def change_brightness(self, color, brightness):# brightness range [0,127] for RGB color space
        r,g,b = color
        if brightness == 0:
            return (0,0,0)
        else:
            brightness = 128 - brightness
            return (r//brightness,g//brightness,b//brightness)      
    
    def set_all(self,color,brightness=255):
        if brightness == 255:
            self.aled.fill(color)
        else:
            self.aled.fill(self.change_brightness(color, brightness))
    
    def clear_all(self,color = (0,0,0)):
        self.aled.fill(color)
    
    def show(self):
        self.aled.write()
        
    def rgb_color(self, color, color_space):
        '''
        # converts and returns color in 8-bit (R,G,B) format
        # range of color for color_space = RGB: (Red, Green, Blue)
        # range of color for color_space = HSV : (hue [0..360], saturation [0..1], value [0..1]
        # range of color for color_space = C_W : position in degrees on the wheel [0,360], fractions of degrees are allowed
        # range of color for color_space = RGB565: (16-bit color value)
        '''
        if color_space == 'HSV':
            h, s, v = color
            return self.hsv2rgb(h,s,v)     # range of color = (hue [0,360], saturation [0,1], value [0,1]
        elif color_space == 'C_W':
            return self.color_wheel(color) # color = position on the wheel
        # dodac w poźniejszym terminie inne przestrzenie kolorów
        elif color_space = 'RGB565':
            return self.rgb565_to_rgb(color)
        else:
            return color
    
    def set_strip_pixel(self, index, color):
        self.aled.__setitem__(index, color)      
      
    def set_strip_pixels(self, index_begin, index_end, color, step=1):
        for index in range (index_begin, index_end, step):
            self.set_strip_pixel(index, color)
    
    def set_matrix_pixel(self, index_x, index_y, color):
        self.aled.__setitem__(self.matrix[index_x][index_y], color)
        
    def set_matrix_pixels(self, index_x_begin, index_y_begin, index_x_end, index_y_end,  color, step = 1):
        for index in range (self.matrix[index_x_begin][index_y_begin],self.matrix[index_x_end][index_y_end],step):
            self.set_strip_pixel(index,color)
    
    def get_matrix_index(self,x,y):
        return self.matrix[x][y]
    
    # HSV: Hue, Saturation, Value
    # H: position in the spectrum
    # S: color saturation ("purity")
    # V: color brightness
    
    def rgb2hsv(self,red,green,blue):       
        t = time.ticks_us()
        Red, Green, Blue = red/255, green/255, blue/255
        print(Red, Green, Blue)
        Hue = -1
        Saturation= -1
        maximum = max(Red, Green, Blue)
        minimum = min(Red, Green, Blue)
        delta = maximum - minimum
        #Lightness = (maximum+minimum)/2
        # calculation of hue
        if delta == 0:
            Hue = 0
        elif maximum == Red:
            Hue = 60*(((Green - Blue)/delta)%6)
        elif maximum == Green:
            Hue = 60*(2+(Blue - Red)/delta)
        elif maximum == Blue:
            Hue = 60*(4+(Red - Green)/delta)
        #calculation of saturation
        if maximum == 0:
            Saturation = 0
        else:
            Saturation = (delta/maximum)*100
        #calculation of value
        Value = maximum*100
        print(time.ticks_diff(time.ticks_us(),t))
        return (round(Hue), round(Saturation), round(Value))
        
    def hsv2rgb (self, hue, saturation, value):
        # source : WIKIPEDIA https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
  
        Chroma = value * saturation    #calculation fo chroma
        X = Chroma*(1-abs((hue/60)%2-1)) # intermediate value
        m = value - Chroma  #extra value
        if 0 <= hue < 60:
            Red, Green, Blue = Chroma, X, 0
        elif 60 <= hue < 120:
            Red, Green, Blue = X, Chroma, 0
        elif 120 <= hue < 180:
            Red, Green, Blue = 0, Chroma, X
        elif 180 <= hue < 240:
            Red, Green, Blue = 0, X, Chroma
        elif 240 <= hue < 300:
            Red, Green, Blue = X, 0, Chroma
        elif 300 <= hue < 360:
            Red, Green, Blue = Chroma, 0, X
        Red, Green, Blue = round((Red + m)*255), round((Green + m)*255), round((Blue + m)*255)
        return (Red, Green, Blue)


    def color_wheel(self,pos):
        # pos in range [0,255]
        t = time.ticks_us()
        if pos <= 85:
            return (pos*3, 255-pos*3, 0)
        elif pos <= 170:
            pos -= 85
            return (255-pos*3, 0, pos*3)
        else:
            pos -= 170
            return (0, pos*3, 255-pos*3)
    
    def rgb_to_rgb565(self,color):
        # Extract the red, green, and blue components from the RGB color
        red, green, blue = color

        # Scale the color components from 8 bits to 5/6/5 bits
        red = (red >> 3) & 0x1F
        green = (green >> 2) & 0x3F
        blue = (blue >> 3) & 0x1F

        # Pack the color components into the RGB565 format
        return (red << 11) | (green << 5) | blue
    
    def rgb565_to_rgb(self,color):
        # Extract the red, green, and blue components from the RGB565 color
        red = (color >> 11) & 0x1F
        green = (color >> 5) & 0x3F
        blue = color & 0x1F

        # Scale the color components from 5/6/5 bits to 8 bits
        red = (red << 3) | (red >> 2)
        green = (green << 2) | (green >> 4)
        blue = (blue << 3) | (blue >> 2)

        # Pack the color components into the RGB format
        return (red, green, blue)
    
    def led_matrix(self, lightning_form, x, y):
        self.leds_count = x * y
        self.matrix = []
        if lightning_form == 'chain_matrix':
            for xx in range (x):
                col = []
                for yy in range (y):      
                    if xx%2 == 0:
                        val = (xx*y)+yy
                        col.append(val)
                    else:
                        val = ((xx*y)+y)-yy-1
                        col.append(val)
                self.matrix.append(col)
        else:
            for xx in range (x):
                col = []
                for yy in range (y):
                    val = (xx*y)+yy
                    col.append(val)
                self.matrix.append(col)       
    
    def round_cooridinates(self, coordinates):
        # rounds coordinates for matrix indices
        points_rounded = []
        for point in cooridnates:
            points_rounded.append((round(point[0]),round(point[1])))
        return points_rounded
        

